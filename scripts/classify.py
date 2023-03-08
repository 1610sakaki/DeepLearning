# ライブラリのインポート
import csv
import os
import shutil

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nbformat import write
from operate import OperateDir

"""
IMG_LIST = ['/home/mt-sakaki/DEVELOPMENT/project1/izumi04_img/sort_folder/type4/01_ok/220607_080355_0000000069_CAM1_COLOR_OK.jpg',
            '/home/mt-sakaki/DEVELOPMENT/project1/izumi04_img/sort_folder/type4/01_ok/220607_112647_0000004471_CAM1_COLOR_OK.jpg',
            '/home/mt-sakaki/DEVELOPMENT/project1/izumi04_img/sort_folder/type4/01_ok/220607_112711_0000004482_CAM1_COLOR_OK.jpg',
            '/home/mt-sakaki/DEVELOPMENT/project1/izumi04_img/sort_folder/type4/01_ok/220607_080141_0000000013_CAM1_COLOR_OK.jpg',
            '/home/mt-sakaki/DEVELOPMENT/project1/izumi04_img/sort_folder/type4/01_ok/220607_090422_0000001065_CAM1_COLOR_OK.jpg',
            '/home/mt-sakaki/DEVELOPMENT/project1/izumi04_img/sort_folder/type4/01_ok/220607_081631_0000000305_CAM1_COLOR_OK.jpg'
            ]
"""
FPATH = "/mnt/c/Users/sakakih/Desktop/Download/220621/color_ok"
MOVE2FILE = "/mnt/c/Users/sakakih/Desktop/Download/220621/03_miss_reclass"
JUDGE_RATE = 3

fig = plt.figure(dpi=150)


def get_fpath(fpath):  # ファイルのパスをリスト化
    model = OperateDir()
    img_list = model.all_file(fpath)
    for index, fname in enumerate(img_list):
        fname = os.path.join(FPATH, fname)
        img_list[index] = fname
    return img_list


def fig_plot(i, output):  # 確認でイメージを可視化
    try:
        ax = plt.subplot(2, 3, i + 1)  # 表示位置の指定
        ax.imshow(output)  # イメージの表示
        ax.set_xticks([])  # x軸の目盛りを非表示
        ax.set_yticks([])  # y軸の目盛りを非表示
    except Exception:
        pass


def output_csv(outfile, csv_list):  # 結果をcsvに出力

    with open(outfile, "a") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(csv_list)


def detect_white(img_list):  # 対象の色をRGBを指定して判定する
    for i, image in enumerate(img_list):
        flag = 0  # ファイルを移動させるか判定するフラグ
        csv_list = []
        img = cv2.imread(image, 1)  # 画像を読み込む
        img_trim = img[175:1030, 370:1240]  # 必要範囲で切り抜き
        img = cv2.cvtColor(img_trim, cv2.COLOR_BGR2RGB)  # RGB並び替え

        img_array = np.asarray(img)  # numpy配列に変換

        # 色の範囲を指定する
        lower_color = np.array([200, 200, 200])
        upper_color = np.array([255, 255, 255])

        # 指定した色に基づいたマスク画像の生成
        mask = cv2.inRange(img_array, lower_color, upper_color)
        output = cv2.bitwise_and(img_array, img_array, mask=mask)

        # 白い範囲をカウント
        white_area = 0
        # 全体の画素数
        whole_area = output.shape[0] * output.shape[1]

        # 行数取得
        height = output.shape[0]
        width = output.shape[1]

        # 画像の３値化と各色の面積比を求める
        for j in range(height):
            for k in range(width):
                if np.any(output[j, k] > lower_color):
                    white_area += 1

        # 白の割合を計算＆出力
        rate = round(white_area / whole_area * 100, 2)
        csv_list.append(image)
        csv_list.append(rate)

        # 判定でフラグがたてばファイルを移動
        if rate >= JUDGE_RATE:
            shutil.move(image, MOVE2FILE)
            flag = "move"
        else:
            flag = "unmove"
        csv_list.append(flag)

        # print('IMAGE='+image, '    ', 'White_Area=' + str(rate)+'%', '    ', 'flag=', flag)

        # 判定をcsvに記録
        output_csv("out.csv", csv_list)

        # 確認用で可視化
        fig_plot(i, output)
    # fig_plotの結果を表示
    # plt.show()


def main():
    img_list = get_fpath(FPATH)
    detect_white(img_list)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
#
# usage: python3 image.py
# objective: 画像を回転やノイズを加えることで複製する
#

import os

import cv2
import numpy as np
from operate import OperateDir

DIR_PATH = "/home/mt-sakaki/DeepLearning/scripts/正面"
# DIR_PATH = "/home/mt-sakaki/DeepLearning/smp/"

CNT = 0


def equalizeHistRGB(src):  # ヒストグラム均一化

    RGB = cv2.split(src)
    """
    Blue = RGB[0]
    Green = RGB[1]
    Red = RGB[2]
    """
    for i in range(3):
        cv2.equalizeHist(RGB[i])

    img_hist = cv2.merge([RGB[0], RGB[1], RGB[2]])
    return img_hist


def addGaussianNoise(src):  # ガウシアンノイズ

    row, col, ch = src.shape
    mean = 0
    # var = 0.1
    sigma = 15
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = src + gauss

    return noisy


def addSaltPepperNoise(src):  # salt&pepperノイズ

    row, col, ch = src.shape
    s_vs_p = 0.5
    amount = 0.004
    out = src.copy()
    # Salt mode
    num_salt = np.ceil(amount * src.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in src.shape]
    out[coords[:-1]] = (255, 255, 255)

    # Pepper mode
    num_pepper = np.ceil(amount * src.size * (1.0 - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in src.shape]
    out[coords[:-1]] = (0, 0, 0)
    return out


def make_multiimage(dir_path, fname):
    # ルックアップテーブルの生成
    average_square = (3, 3)
    """
    min_table = 50
    max_table = 205
    diff_table = max_table - min_table
    gamma1 = 0.75
    gamma2 = 1.5

    LUT_HC = np.arange(256, dtype="uint8")
    LUT_LC = np.arange(256, dtype="uint8")
    LUT_G1 = np.arange(256, dtype="uint8")
    LUT_G2 = np.arange(256, dtype="uint8")

    # LUTs = []
    # 平滑化用【ぼかし】

    # ハイコントラストLUT作成
    for i in range(0, min_table):
        LUT_HC[i] = 0

    for i in range(min_table, max_table):
        LUT_HC[i] = 255 * (i - min_table) / diff_table

    for i in range(max_table, 255):
        LUT_HC[i] = 255

    # その他LUT作成
    for i in range(256):
        LUT_LC[i] = min_table + i * (diff_table) / 255
        LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)
        LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)

    # LUTs.append(LUT_HC)
    # LUTs.append(LUT_LC)
    # LUTs.append(LUT_G1)
    # LUTs.append(LUT_G2)
    """

    # 画像の読み込み
    img = os.path.join(dir_path, fname)
    img_src = cv2.imread(img, 1)

    trans_img = []

    try:
        trans_img.append(img_src)  # オリジナル画像
    except Exception:
        print("miss")
    print("trans_img", len(trans_img))

    # LUT変換
    """
    try:
        for i, LUT in enumerate(LUTs):
            trans_img.append(cv2.LUT(img_src, LUT))
    except Exception:
        print("miss")
    print("trans_img", len(trans_img))
    """

    # 平滑化
    try:
        trans_img.append(cv2.blur(img_src, average_square))
    except Exception:
        print("ミス")
        pass
    print("trans_img", len(trans_img))

    # ヒストグラム均一化
    """
    try:
        trans_img.append(equalizeHistRGB(img_src))
    except Exception:
        print("ミス")
        pass
    print("trans_img", len(trans_img))
    """

    # ノイズ付加
    try:
        trans_img.append(addGaussianNoise(img_src))
        # trans_img.append(addSaltPepperNoise(img_src))
    except Exception:
        print("ミス")
        pass

    print("trans_img", len(trans_img))

    # 反転
    flip_img = []
    for img in trans_img:  # 上記で作成した7種類の複製画像をさらに反転を加えて水増しする
        flip_img.append(cv2.flip(img, 1))  # 左右反転
        flip_img.append(cv2.flip(img, 0))  # 上下反転
        flip_img.append(cv2.flip(img, -1))  # 上下左右反転
        print("flip_img:", len(flip_img))
    trans_img.extend(flip_img)  # 引数に渡された別のリストを追加してリストを拡張
    print("trans_img", len(trans_img))

    return img_src, trans_img


def save_image(img_src, trans_img, dir_path, fname):  # 保存
    trans_images = os.path.join(dir_path, "trans_images")
    if not os.path.exists(trans_images):
        os.mkdir(trans_images)
    base = os.path.splitext(os.path.basename(fname))[0] + "_"
    img_src.astype(np.float64)
    for i, img in enumerate(trans_img):
        # 比較用
        # cv2_hconcat = cv2.hconcat([img_src.astype(np.float64), img.astype(np.float64)])
        # cv2.imwrite("trans_images/" + base + str(i) + ".jpg" ,cv2_concat)
        fpath = os.path.join(trans_images, base + str(i) + ".jpg")
        # img = img / 255  # 正規化
        cv2.imwrite(fpath, img)  # 多次元配列(numpy.ndarray)情報を元に、画像を保存
        print(fpath)


def main(dir_path):
    ope = OperateDir(dir_path, 0, 1, 2)
    flist = ope.all_file()
    for fname in flist:
        print(fname)
        img_src, trans_img = make_multiimage(dir_path, fname)
        save_image(img_src, trans_img, dir_path, fname)


if __name__ == "__main__":
    main(DIR_PATH)

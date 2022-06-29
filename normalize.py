# -*- coding: utf-8 -*-
#
# usage: python3 normalize.py
# objective: 画像を正規化する
#

import cv2
import os
from operate import OperateDir
import matplotlib.pyplot as plt

DIR_PATH = '/home/mt-sakaki/DEVELOPMENT/AI_PROJECT/IMAGE/ORG_IMAGE/izumi04_img/sorted/type5/05_normalization/trans_images'


def main(dir_path):
    ope = OperateDir()
    flist = ope.all_file(dir_path)
    for fname in flist:
        fpath = os.path.join(dir_path, fname)
        img = cv2.imread(fpath, 1)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img - 50
        plt.imshow(img)
        cv2.imwrite(fpath, img)  # 多次元配列(numpy.ndarray)情報を元に、画像を保存
        print(fpath)
        # plt.show()


if __name__ == '__main__':
    main(DIR_PATH)

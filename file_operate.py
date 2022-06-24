import os
import shutil

COLOR_OK = '../izumi04_img/220607/color_ok'
COLOR_NG = '../izumi04_img/220607/color_ng'
ORIGINAL_NG = '../izumi04_img/220607/original_ng'

TYPE4_01OK = '../izumi04_img/sort_folder/type4/01_ok'
TYPE4_02NG = '../izumi04_img/sort_folder/type4/02_ng'
TYPE4_03MISS = '../izumi04_img/sort_folder/type4/03_miss'

MISS_TARGET = ['084352', '081655', '082538', '084354',
               '085439', '090129', '091924', '092726']

NG_TARGET = ['COLOR']


class OperateDir():
    def __init__(self):
        self.cnt = 0

    def all_file(self, dir_path):  # すべてのファイル名とファイル数を出力
        file_list = []
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                file_list.append(path)
                self.cnt += 1
        return file_list

    def target_file(self, dir_path, target):  # 特定のファイル名とファイル数を出力
        file_list = []
        for path in os.listdir(dir_path):
            for i in range(len(target)):
                if os.path.isfile(os.path.join(dir_path, path)) and target[i] in path:
                    file_list.append(path)
                    self.cnt += 1
        return file_list

    def copy_file(self, file_list, dir_path, tgt_dir):  # ファイルをコピーさせる
        for fname in file_list:
            fname = os.path.join(dir_path, fname)
            shutil.copy(fname, tgt_dir)
            # print(fname)

    def move_file(self, file_list, dir_path, tgt_dir):  # ファイルを移動させる
        for fname in file_list:
            fname = os.path.join(dir_path, fname)
            shutil.move(fname, tgt_dir)

    def delete_file(self, tgt_flist, dir_path, target):  # 指定のファイルを削除する
        for fname in tgt_flist:  # 対象のフォルダ内のファイルを一個ずつ見る
            for i in range(len(target)):
                if target[i] in fname:  # ファイルが削除対象に入っているか？
                    print(target[i])
                    fname = os.path.join(dir_path, fname)  # ファイルパス結合
                    os.remove(fname)  # ファイル削除
                    self.cnt += 1


def main():
    # インスタンス化
    model = OperateDir()

    # ミス判定をコピー
    flist_miss = model.target_file(COLOR_OK, MISS_TARGET)
    model.copy_file(flist_miss, COLOR_OK, TYPE4_03MISS)

    # OK判定をコピー
    flist_ok = model.all_file(COLOR_OK)
    model.copy_file(flist_ok, COLOR_OK, TYPE4_01OK)
    model.delete_file(flist_ok, COLOR_OK, MISS_TARGET)

    # NG判定をコピー
    flist_ng = model.target_file(ORIGINAL_NG, NG_TARGET)
    model.copy_file(flist_ng, ORIGINAL_NG, TYPE4_02NG)

    #print(*flist_ng, sep='\n')


if __name__ == '__main__':
    main()

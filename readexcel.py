import os
import glob
import pandas as pd
import datetime as dt
import shutil


EXCEL_PATH = '/mnt/c/Users/sakakih/Desktop/Download/コピークロス合否.xls'
EXCEL_PATH2 = '/mnt/c/Users/sakakih/Desktop/Download/01_クロスまとめ.xlsx'
DOWNLOAD_PATH = '/mnt/c/Users/sakakih/Desktop/Download/izumi04s_OK/color_ok/*'
SKIPROWS = 2


def read_excel():
    df = pd.read_excel(EXCEL_PATH, sheet_name='メインセンサー', skiprows=SKIPROWS)
    df = df.drop(df.columns[7:9], axis=1)
    df = df.drop(df.columns[10:12], axis=1)
    df = df.drop(df.index[4:15541], axis=0)
    drop_index = df.index[df['異常有無'] == '異常なし']
    df = df.drop(drop_index)
    df = df[df['成型日付'] > dt.datetime(2022, 6, 10)]
    df.to_csv('format01.csv')

    ls = []
    ls1 = df['カメラ時間'].to_list()
    for i, x in enumerate(ls1):
        ls1[i] = str(x).replace(':', '')

    ls2 = df['成型日付'].to_list()
    for i, x in enumerate(ls2):
        ls2[i] = x.strftime('%Y%m%d')[2:]

    for i in range(len(ls1)):
        ls.append(str(ls2[i]) + '_' + str(ls1[i]))

    target_file = []
    flist = glob.glob(DOWNLOAD_PATH)
    for row in flist:
        for ix in ls:
            if ix in row:
                target_file.append(row)
    print(*target_file, sep='\n')
    print(len(target_file))
    dir_path = '/home/mt-sakaki/DEVELOPMENT/AI_PROJECT/IMAGE/ORG_IMAGE/izumi04_img/miss'
    for row in target_file:
        shutil.copy(row, dir_path)


def read_excel2():
    df = pd.read_excel(EXCEL_PATH2, sheet_name='生産品種')
    df = df.drop(df.index[12:], axis=0)
    df = df.drop(df.columns[0:2], axis=1)
    code_list0 = df['品名コード'].to_list()
    code_list = []
    for x in code_list0:
        if not x in code_list:
            code_list.append(x)
    for num in code_list:
        x = df[df['品名コード'] == num].dropna(how='all', axis=1)
        print(x, '\n'*3)


def main():
    # read_excel()
    read_excel2()


if __name__ == '__main__':
    main()

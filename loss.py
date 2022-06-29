
# objective: 学習過程の損失の変化を可視化
# usage: python3 result.py type4-1

import csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys
DIR_PATH = '/home/mt-sakaki/DEVELOPMENT/AI_PROJECT/csv/resultcsv/'
FNAME = 'loss.csv'
COLUMNS = ['Epoch', 'Loss', 'Best', 'time']
ARGS = sys.argv[1]
EPOCH_MAX = 100


def get_rows(row, df):  # データの前処理
    if 'Epoch' in row[0]:
        row[0] = row[0].replace('Epoch: ', '')
        row[1] = float(row[1].replace('  Loss: ', ''))
        row[2] = float(row[2].replace('  Best: ', ''))
        row[3] = row[3].replace('  ', '')
        row[3] = row[3].replace('msec', '')
        df.loc[len(df)] = row
    if 'Result' in row[0]:
        # print(row)
        pass


def csv_read(path, fname, columns):  # ファイルパス上のcsvデータをpd.DataFrameに変換する
    fpath = os.path.join(path, 'type' + ARGS, fname)
    df = pd.DataFrame(index=[], columns=columns)
    with open(fpath, encoding='utf-8') as file:
        for row in csv.reader(file):
            get_rows(row, df)
    return df, fpath


def df_plot(df, columns):  # データを可視化する
    df.plot(xlim=[0, EPOCH_MAX])
    plt.title('type' + ARGS, fontsize=14)
    plt.xlabel(columns[0], size=16)
    plt.ylabel(columns[1], size=16)
    plt.tick_params(direction='in', labelsize=14)  # 目盛の向きと数値のサイズ
    plt.show()


def main():
    df, fpath = csv_read(DIR_PATH, FNAME, COLUMNS)
    df_plot(df, COLUMNS)


if __name__ == '__main__':
    main()

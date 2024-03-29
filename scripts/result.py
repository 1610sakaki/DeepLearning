
# usage: python3 result.py 4-1
# objective: 学習結果からAIモデルの評価を行う


import csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import sys

DIR_PATH = '/home/mt-sakaki/DEVELOPMENT/AI_PROJECT/csv/resultcsv'
FNAME = 'result.tsv'
EXCEL_PATH = '/mnt/c/Users/sakakih/Desktop/ガラスクロスモデル結果/ガラスクロス品種1_AIモデル開発報告書.xlsx'


def get_rows(row, df):
    # 数値だけを取り出す
    row[1] = int(re.sub(r'\D', '', row[1]))
    if row[1] == 2:
        row[1] = 'OK'
    elif row[1] == 1:
        row[1] = 'NG'
    row[2] = int(re.sub(r'\D', '', row[2]))
    if row[2] == 2:
        row[2] = 'OK'
    elif row[2] == 1:
        row[2] = 'NG'
    row[3] = float(re.sub(r'\D', '', row[3])) / 10
    row.pop(4)
    df.loc[len(df)] = row


def tsv_read(path, fname, columns):  # ファイルパス上のtsvデータをpd.DataFrameに変換する
    fpath = os.path.join(path, 'type' + sys.argv[1], fname)
    df = pd.DataFrame(index=[], columns=columns)
    with open(fpath, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            get_rows(row, df)
    return df


def write_excel(df, i):  # 結果をエクセルに出力
    with pd.ExcelWriter(EXCEL_PATH, mode='a') as writer:
        df.to_excel(writer, sheet_name='type' + sys.argv[1] + '_'+str(i))


def output_dataframe(df):
    # Matplotlibにて表を出力
    fig, ax = plt.subplots(
        figsize=((len(df.columns)+1)*10.4, (len(df)+1)*5.4))
    ax.axis('off')
    tbl = ax.table(cellText=df.values,
                   bbox=[0, 0, 1, 1],
                   colLabels=df.columns,
                   rowLabels=df.index)
    # plt.savefig('table.png') #PNG画像出力
    plt.show()


def main():
    columns = ['IMG_NAME', 'GT(actual)', 'PR(prediction)', 'MATCHING']
    df = tsv_read(DIR_PATH, FNAME, columns)
    df.loc[df[columns[1]] == df[columns[2]], 'JUDGE'] = True  # 正解ならばTrue
    df.loc[df[columns[1]] != df[columns[2]], 'JUDGE'] = False  # 不正解ならばFalse
    false_neg = ((df[columns[1]] == 'OK') & (
        df['JUDGE'] == False)).sum()  # 偽陰性
    false_pos = ((df[columns[1]] == 'NG') & (
        df['JUDGE'] == False)).sum()  # 偽陽性
    true_neg = ((df[columns[1]] == 'NG') & (df['JUDGE'] == True)).sum()  # 真陰性
    true_pos = ((df[columns[1]] == 'OK') & (df['JUDGE'] == True)).sum()  # 真陽性
    print('\n', df)
    # 真陽性のMatching
    df_true_pos = df[(df[columns[1]] == 'OK') & (
        df['JUDGE'] == True)][columns[3]]
    # 偽陽性のMatching
    df_false_pos = \
        df[(df[columns[1]] == 'NG') & (df['JUDGE'] == False)][columns[3]]
    # 真陰性のMatching
    df_true_neg = df[(df[columns[1]] == 'NG') & (
        df['JUDGE'] == True)][columns[3]]
    # 偽陰性のMatching
    df_false_neg = \
        df[(df[columns[1]] == 'OK') & (df['JUDGE'] == False)][columns[3]]

    # 評価指標の混同行列(Confusion Matrix)
    df_2 = pd.DataFrame(index=[], columns=['prediction_NG', 'prediction_OK'])
    row1 = [[true_neg, df_true_neg.max(), df_true_neg.min()],
            [false_pos, df_false_pos.max(), df_false_pos.min()]]
    row2 = [[false_neg, df_false_neg.max(), df_false_neg.min()],
            [true_pos, df_true_pos.max(), df_true_pos.min()]]
    df_2.loc['actual_NG'] = row1
    df_2.loc['actual_OK'] = row2
    print('\n', df_2)

    # その他の評価指数
    df_3 = pd.DataFrame(index=[], columns=['value', 'Description'])
    accuracy = (true_pos+true_neg)/(true_pos+false_pos+true_neg+false_neg)
    precision = true_pos/(true_pos+false_pos)
    tpr = true_pos/(true_pos+false_neg)
    f_measure = (2*precision*tpr) / (tpr + precision)
    tnr = true_neg/(true_neg+false_pos)
    fpr = false_pos/(false_pos+true_neg)
    df_3.loc['Accuracy'] = [
        round(accuracy*100, 1), '全ての予測のうち、正解した予測の割合']  # 正解率
    df_3.loc['Precision'] = [
        round(precision*100, 1), '陽性と予測したもののうち、実際に陽性であるものの割合']  # 適合率
    df_3.loc['TPR'] = [
        round(tpr*100, 1), '実際に陽性であるもののうち、正しく陽性と予測できたものの割合']  # 再現率
    df_3.loc['f-measure'] = [round(f_measure*100, 1),
                             '対照的な特徴を持つ適合率と再現率の調和平均']  # F値
    df_3.loc['TNR'] = [
        round(tnr*100, 1), '実際に陰性であるもののうち、正しく陰性と予測できたものの割合']  # 特異率
    df_3.loc['FPR'] = [
        round(fpr*100, 1), '実際には陰性であるもののうち、誤って陽性と予測したものの割合']  # 偽陽性率
    print('\n', df_3)
    # output_dataframe(df_2)
    df.to_csv('out.csv')
    df_2.to_csv('out2.csv')
    df_3.to_csv('out3.csv')
    '''
    write_excel(df, 1)
    write_excel(df_2, 2)
    write_excel(df_3, 3)
    '''


if __name__ == '__main__':
    main()

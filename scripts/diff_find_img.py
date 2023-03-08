import cv2
import matplotlib.pyplot as plt


def make_hist(img):
    # カラーリスト
    colorList = ["blue", "green", "red"]

    for i, j in enumerate(colorList):
        # ヒストグラム
        hist = cv2.calcHist(
            images=[img],  # 画像データを指定
            channels=[i],  # ヒストグラムを計算する画像のチャンネルのインデックス
            mask=None,  # マスク画像｜全画素のヒストグラムを計算する場合 “None” を指定
            histSize=[256],  # ビン数
            ranges=[0, 256],  # ヒストグラムの範囲
        )
        # 可視化
        plt.plot(hist, color=j)


# 画像読み込み、グレースケール化
img_1 = cv2.imread(
    "/home/mt-sakaki/DeepLearning/smp/trans_images/sample_fruit_0.jpg", 1
)
img_2 = cv2.imread(
    "/home/mt-sakaki/DeepLearning/smp/trans_images/sample_fruit_2.jpg", 1
)
make_hist(img_1)
plt.show()
make_hist(img_2)
plt.show()
img_1_gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
img_2_gray = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

# 画像を引き算
img_diff = cv2.absdiff(img_1_gray, img_2_gray)

# 2値化
ret2, img_th = cv2.threshold(img_diff, 20, 255, cv2.THRESH_BINARY)

# 輪郭を検出
contours, hierarchy = cv2.findContours(
    img_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# 閾値以上の差分を四角で囲う
for i, cnt in enumerate(contours):
    x, y, width, height = cv2.boundingRect(cnt)
    if width > 50 or height > 50:
        cv2.rectangle(img_1, (x, y), (x + width, y + height), (0, 0, 255), 1)

cv2.imwrite("diff_box最終.jpg", img_1)

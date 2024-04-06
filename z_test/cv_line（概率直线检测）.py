import math

import cv2
import numpy as np

from core import file_locator


def bettwen(t):
    return math.degrees(t)

def limit(i,t,interval=1):
    return t-interval<i<t+interval


img = cv2.imread('s.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 150, apertureSize=3)

lines = cv2.HoughLinesP (edges, 0.5, np.pi / 180, 50,minLineLength=300,maxLineGap=50)

newi=np.zeros(img.shape)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(newi,(x1,y1),(x2,y2),(0,255,0),1)

print(len(lines))
import cv2
import numpy as np
from sklearn.cluster import DBSCAN

# # 假设您已经有了 lines 变量，其中包含检测到的线段
# # lines 是一个 N x 1 x 4 的数组，每个元素是一个线段的端点坐标 (x1, y1, x2, y2)
#
# # 将线段的端点坐标转换为特征向量
# features = np.array(lines).reshape(-1, 4)
#
# # 使用 DBSCAN 进行聚类
# dbscan = DBSCAN(eps=10, min_samples=2)
# labels = dbscan.fit_predict(features)
#
# # 合并同一簇中的线段
# merged_lines = []
# for label in np.unique(labels):
#     cluster_lines = features[labels == label]
#     avg_x1 = np.mean(cluster_lines[:, 0])
#     avg_y1 = np.mean(cluster_lines[:, 1])
#     avg_x2 = np.mean(cluster_lines[:, 2])
#     avg_y2 = np.mean(cluster_lines[:, 3])
#     merged_lines.append([avg_x1, avg_y1, avg_x2, avg_y2])
#
# # 将合并后的线段绘制在图像上
# for x1, y1, x2, y2 in merged_lines:
#     cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

# # 显示图像
# cv2.imshow("Merged Lines", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('houghlines3.jpg', newi)



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

lines = cv2.HoughLinesP (edges, 0.5, np.pi / 180, 50,maxLineGap=10)

for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
# for line in lines:
#     rho, theta = line[0]
#     print(rho, theta)
#     # if math.fabs(rho)<100:
#     #     continue
#     # 并不是毫无意义，此处测量出结果是60/120度是标准直线
#     if  not limit(bettwen(theta),120,10) and not  limit(bettwen(theta),60,10):
#         continue
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a * rho
#     y0 = b * rho
#     x1 = int(x0 + 1000 * (-b))
#     y1 = int(y0 + 1000 * (a))
#     x2 = int(x0 - 1000 * (-b))
#     y2 = int(y0 - 1000 * (a))
#
#     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#     cv2.putText(img, str(bettwen(theta)), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (128, 128, 128), 2, cv2.LINE_AA)

cv2.imwrite('houghlines3.jpg', img)

def rotate_image(image, angle):
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image


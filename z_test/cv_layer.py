import cv2
import numpy as np
from PIL import Image

# 读取图像
img = Image.open('screen_now.png')
# 对图像进行模糊操作
blur = cv2.blur(np.array(img), (5, 5))
blur0 = cv2.medianBlur(blur, 5)
blur1 = cv2.GaussianBlur(blur0, (5, 5), 0)
blur2 = cv2.bilateralFilter(blur1, 9, 75, 75)
# 将图像转换为HSV色彩空间
hsv = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
# 设置蓝色的阈值范围
low_blue = np.array([100, 148, 120])
high_blue = np.array([180, 255, 180])

# 创建一个掩膜
mask = cv2.inRange(hsv, low_blue, high_blue)

# 将掩膜应用到原始图像上
res = cv2.bitwise_and(np.array(img), np.array(img), mask=mask)
# 显示结果图像
cv2.imshow('提取的鸟部分', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

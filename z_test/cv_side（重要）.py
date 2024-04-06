import sys

import cv2
import numpy as np

from core import config, screen_locator, file_locator, work_flow

apple = cv2.imread(file_locator.get_cache_screenshot())

image = cv2.cvtColor(apple, cv2.COLOR_BGR2GRAY)
image_copy = apple.copy()

retval, dst = cv2.threshold(image, 80, 120, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2)

# 创建一个空的灰度图像
gray_image = np.zeros(dst.shape, dtype=np.uint8)

cv2.imshow('111', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

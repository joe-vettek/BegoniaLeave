import cv2
import numpy as np

from core import file_locator, work_flow

apple = cv2.imread(file_locator.get_cache_screenshot())
image = cv2.cvtColor(apple, cv2.COLOR_BGR2GRAY)
gs = np.zeros(apple.shape)
gs = gs.astype(np.uint8)


def anyb(a):
    rs = True
    for i in a:
        if not 92 > i > 83:
            rs = False
    return rs


# for i, g in enumerate(apple):
#     for j, l in enumerate(g):
#         # gs[i,j]=apple[i, j][0]
#         # 蓝色
#         # gs[i, j] = 200 if 150 > apple[i, j][0] > 110 and not 150 > apple[i, j][1] > 110 else 1
#         # 绿色
#         # gs[i, j] = 200 if 150 > apple[i, j][1] > 110 else 1
#         # 红色
#         # gs[i, j] = 200 if 170 > apple[i, j][2] > 115 else 1
#         # 黄色
#         # gs[i, j] = 150 if 220 > (image[i, j]) > 150 else 0
#         # 脚底
#         # gs[i, j] = 255 if anyb(apple[i, j]) else 1
#         # 边线
#         gs[i, j] = 255 if 256 > (image[i, j]) > 220 else 0

from PIL import Image

# a, b = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)
# third_dimension_values = apple[:, :, 0]>92+apple[:, :, 1]>92+apple[:, :, 2]>92
yellow = np.where((220 > image) & (image > 150), 255, 0)
Image.fromarray(yellow).convert('L').save('s_yellow.jpg')
# 待改进numpy
# foot = np.where(anyb(apple), 255, 0)
# Image.fromarray(yellow).convert('L').save('s_foot.jpg')
# 提高到220可以略去灰色区域
s = np.where((256 > image) & (image > 220), 255, 0)
Image.fromarray(s).convert('L').save('s.jpg')

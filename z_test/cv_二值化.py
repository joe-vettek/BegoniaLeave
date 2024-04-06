import cv2
import numpy as np

apple = cv2.imread('mask.jpg')
image = cv2.cvtColor(apple, cv2.COLOR_BGR2GRAY)
gs = np.zeros(apple.shape)
gs = gs.astype(np.uint8)
for i, g in enumerate(apple):
    for j, l in enumerate(g):
        gs[i, j] = 255 if image[i, j]>100 else 0
from PIL import Image

Image.fromarray(gs).convert('L').save('mask-2.jpg')
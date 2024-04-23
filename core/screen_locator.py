import asyncio
import json
import os
import random

import cv2
import numpy as np

from core import work_flow, log, file_locator,mfw_handler

# from core.mfw_handler import *

# 屏幕缩放系数 mac缩放是2 windows一般是1
screenScale = 1


def read_img(img_path):
    return cv2.imread(img_path)


# : cv2.typing.MatLike for >4.6
def ImageMatchInScreen(target: np.ndarray, temp: np.ndarray, debug=False):
    theight, twidth = target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    if debug:
        print("目标图宽高：" + str(twidth) + "-" + str(theight))
        print("模板图宽高：" + str(tempwidth) + "-" + str(tempheight))
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp = cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    stempheight, stempwidth = scaleTemp.shape[:2]
    # print("缩放后模板图宽高：" + str(stempwidth) + "-" + str(stempheight))
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if debug:
        print("精度：" + str(max_val))
    if (max_val >= 0.9):
        # 计算出中心点
        top_left = max_loc
        bottom_right = (top_left[0] + twidth, top_left[1] + theight)
        tagHalfW = int(twidth / 2)
        tagHalfH = int(theight / 2)
        tagCenterX = top_left[0] + tagHalfW
        tagCenterY = top_left[1] + tagHalfH
        # 左键点击屏幕上的这个位置
        # pyautogui.click(tagCenterX, tagCenterY, button='left')
        return tagCenterX, tagCenterY
    else:
        return None


def ImageMatchInScreenMult(target: np.ndarray, temp: np.ndarray, mask=None, debug=False):
    theight, twidth = target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    if debug:
        print("目标图宽高：" + str(twidth) + "-" + str(theight))
        print("模板图宽高：" + str(tempwidth) + "-" + str(tempheight))
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp = cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    stempheight, stempwidth = scaleTemp.shape[:2]
    # print("缩放后模板图宽高：" + str(stempwidth) + "-" + str(stempheight))
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED, mask)
    loc = np.where(res >= 0.9)
    if len(loc[0]) > 0:
        # 计算出中心点
        if debug:
            tagHalfW = int(stempwidth / 2)
            tagHalfH = int(stempheight / 2)
        else:
            tagHalfW = int(stempwidth * (random.random() * 0.6 + 0.2))
            tagHalfH = int(stempheight * (random.random() * 0.6 + 0.2))
        result = []
        for pt in zip(*loc[::-1]):
            result.append((float(pt[0] + tagHalfW), float(pt[1] + tagHalfH)))
        # 左键点击屏幕上的这个位置
        # pyautogui.click(tagCenterX, tagCenterY, button='left')
        return result
    else:
        return None


def run_check(target: np.ndarray, temp: np.ndarray, mask=None):
    point_color = (0, 255, 255)  # BGR
    poss = ImageMatchInScreenMult(target, temp, debug=True, mask=mask)
    if poss:
        for p in poss:
            cv2.circle(target, (int(p[0]), int(p[1])), 20, point_color, 0)
    print("找到了", poss)
    cv2.namedWindow("image")
    cv2.imshow('image', target)
    cv2.waitKey(0)  # 显示 10000 ms 即 10s 后消失
    cv2.destroyAllWindows()


# 初始化OCR
# ocr = PaddleOCR(use_angle_cls=True, lang="ch",
#                 show_log=False)  # need to run only once to download and load model into memory


# def text_locations(target: np.ndarray, score=0.5):
#     # text_info_list = ocr.ocr(target, cls=False)
#     text_info_list=ocr_text()
#     if text_info_list is not None:
#         text_info_list = [c for c in text_info_list[0] if c[-1][-1] > score]
#     return text_info_list


def text_center(target: np.ndarray, score=0.5, random_use=True, text_filter=None,roi=None):
    text_list = mfw_handler.ocr_text(text_filter,roi=roi)
    if text_list is not None:
        text_list = text_list["filtered"]
        text_list = [[(int(sum([c["box"][0], c["box"][2] / 2.0]) + 5 * random.random()),
                       int(sum([c["box"][1], c["box"][3] / 2.0]) + 5 * random.random())), c["score"], c["text"]] for c
                     in
                     text_list]
    return text_list


def quick_screenshot():
    return work_flow.WorkFlow().update_screenshot()

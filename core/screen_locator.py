import asyncio
import json
import os
import random

import cv2
import numpy as np

from core import work_flow, log, file_locator

from typing import Tuple
from bin.mfw.maa.define import RectType, MaaAdbControllerTypeEnum
from bin.mfw.maa.library import Library
from bin.mfw.maa.resource import Resource
from bin.mfw.maa.controller import AdbController
from bin.mfw.maa.instance import Instance
from bin.mfw.maa.toolkit import Toolkit, AdbDevice

from bin.mfw.maa.custom_recognizer import CustomRecognizer
from bin.mfw.maa.custom_action import CustomAction

# 屏幕缩放系数 mac缩放是2 windows一般是1
screenScale = 1
maa_inst: Instance = None
controller: AdbController = None
resource: Resource = None
adb_path = "127.0.0.1:5555"


class MyRecognizer(CustomRecognizer):
    def analyze(
            self, context, image, task_name, custom_param
    ) -> Tuple[bool, RectType, str]:
        return True, (0, 0, 100, 100), "Hello World!"


# <bin.mfw.maa.context.SyncContext object at 0x000001ED6A8D2E20>
# Flag_NoButton1 {}
# Rect(x=109, y=273, w=60, h=20)
# [{"box":[109,273,60,20],"score":0.999905,"text":"应用中心"},{"box":[310,273,62,20],"score":0.999958,"text":"系统应用"},{"box":[445,112,103,19],"score":0.999622,"text":"搜索游戏和应用"}]

cache_info = None


class MyAction(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print(context, task_name, custom_param, box, rec_detail)
        global cache_info
        cache_info = rec_detail
        return True

    def stop(self) -> None:
        pass


my_rec = MyRecognizer()
my_act = MyAction()


def ocr_text(txt):
    try:
        global cache_info
        cache_info = None
        asyncio.run(maa_inst.run_task("Flag_NoButton1", {"Flag_NoButton1": {"recognition": "OCR",
                                                                            "text": txt, "action": "Custom",
                                                                            "custom_action": "MyAct"}}))
        if type(cache_info) is str:
            cache_info = json.loads(cache_info)

    except:
        pass
    return cache_info


def cancel_instance():
    global maa_inst, controller
    if maa_inst:
        maa_inst.stop()
    maa_inst = None
    controller = None


async def init_instance():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [await asyncio.create_task(init_resource(), name="init_resource"),
             await asyncio.create_task(init_adb(), name="init_adb"),
             await asyncio.create_task(init_maa(), name="init_maa")]
    return tasks, loop
    # print(await maa_inst.run_task("Flag_NoButton1", {"Flag_NoButton1": {"recognition": "OCR",
    #                                                                     "text": "白夜极光", "action": "Custom",
    #                                                                     "custom_action": "MyAct"}}))


async def init_resource():
    global resource
    version = Library.open(file_locator.get_mfw_bin())
    log.printLog(f"发现 MaaFramework Version: {version}")
    Toolkit.init_config()
    resource = Resource()
    await resource.load(file_locator.get_mfw_res())
    log.printLog("资源加载完毕")


async def init_adb():
    global controller, adb_path
    device_cache = file_locator.get_device()
    if not os.path.exists(device_cache):
        # 暂停扫盘
        # device_list = await Toolkit.adb_devices()
        with open(device_cache, 'w') as file:
            txt = json.dumps([{"address": "127.0.0.1:5555"}, {"address": "127.0.0.1:16384"}])
            file.write(txt)
    else:
        with open(device_cache, 'r') as file:
            device_list = [AdbDevice(adb_path=file_locator.get_adb_name(), address=i["address"],
                                     name=None, controller_type=None,
                                     config=None) for i in json.loads(file.read())]
    # print(device_list)
    if not device_list:
        print("No ADB device found.")
        # exit()
        return False
    device = device_list[0]
    adb_path = str(device.address)
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
        type=MaaAdbControllerTypeEnum.Screencap_FastestWay,
        agent_path=file_locator.get_mfw_agent()
    )
    await controller.connect()
    print(controller)
    log.printLog("已连接到模拟器")


async def init_maa():
    global maa_inst
    maa_inst = Instance()
    # print(maa_inst, resource, controller)
    maa_inst.bind(resource, controller)

    if not maa_inst.inited:
        print("Failed to init MAA.")
        exit()

    # 这里注册的信息要全局保存，否则变量丢了
    maa_inst.register_recognizer("MyRec", my_rec)
    maa_inst.register_action("MyAct", my_act)
    # log.printLog("MaaFramework 初始化完成")
    # print(await maa_inst.run_task("txt_ocr", {"txt_ocr": {"recognition": "OCR",
    #                                                       "text": "白夜极光", "action": "Custom",
    #                                                       "custom_action": "MyAct"}}))
    log.printLog("已初始化mfw实例")


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


def text_center(target: np.ndarray, score=0.5, random_use=True, text_filter=None):
    text_list = ocr_text(text_filter)
    if text_list is not None:
        text_list = [[(int(sum([c["box"][0], c["box"][2] / 2.0]) + 5 * random.random()),
                       int(sum([c["box"][1], c["box"][3] / 2.0]) + 5 * random.random())), c["score"], c["text"]] for c
                     in
                     text_list]
    return text_list


def quick_screenshot():
    return work_flow.WorkFlow().update_screenshot()

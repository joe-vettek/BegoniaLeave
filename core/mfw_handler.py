import asyncio
import json
import os

from core import log, file_locator

from typing import Tuple
from bin.mfw.maa.define import RectType, MaaAdbControllerTypeEnum
from bin.mfw.maa.library import Library
from bin.mfw.maa.resource import Resource
from bin.mfw.maa.controller import AdbController
from bin.mfw.maa.instance import Instance
from bin.mfw.maa.toolkit import Toolkit, AdbDevice

from bin.mfw.maa.custom_recognizer import CustomRecognizer
from bin.mfw.maa.custom_action import CustomAction

maa_inst: Instance = None
controller: AdbController = None
resource: Resource = None


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


def ocr_text(txt, roi=None):
    try:
        global cache_info
        cache_info = None
        task = {"recognition": "OCR",
                "expected": txt, "action": "Custom",
                "custom_action": "MyAct"}
        if roi is not None:
            task["roi"] = roi
        asyncio.run(maa_inst.run_task("Flag_NoButton1", {"Flag_NoButton1": task}))
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
    # Toolkit.init_config()
    Toolkit.init_option(user_path=file_locator.get_cache_dir())
    resource = Resource()
    await resource.load(file_locator.get_mfw_res())
    log.printLog("资源加载完毕")


async def init_adb(retry=False):
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
    if retry:
        device_list = await Toolkit.adb_devices()
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
        agent_path=file_locator.get_mfw_agent(),
        type =   (
                MaaAdbControllerTypeEnum.Input_Preset_AutoDetect
                | MaaAdbControllerTypeEnum.Screencap_Encode
        )
    )
    await controller.connect()
    # print(controller)
    log.printLog("模拟器连接状态：{}".format(controller.connected))
    if not retry and not controller.connected:
        log.printLog("发现可能存在问题，正在自动检索")
        await init_adb(True)


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

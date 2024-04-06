import os
import signal
from typing import List, Tuple, Union
from bin.mfw.maa.define import RectType
from bin.mfw.maa.library import Library
from bin.mfw.maa.resource import Resource
from bin.mfw.maa.controller import AdbController
from bin.mfw.maa.instance import Instance
from bin.mfw.maa.toolkit import Toolkit, AdbDevice

from bin.mfw.maa.custom_recognizer import CustomRecognizer
from bin.mfw.maa.custom_action import CustomAction

import asyncio

import adbutils

os.remove('bin/mfw/bin/debug/maa.log')
async def main():
    version = Library.open("bin/mfw/bin")
    print(f"MaaFw Version: {version}")
    Toolkit.init_config()
    resource = Resource()
    print(10)
    await resource.load("asset/mfw/resource")
    print(11)
    # device_list = await Toolkit.adb_devices()
    print(22)
    # print(device_list)
    # if not device_list:
    #     print("No ADB device found.")
    #     exit()

    # for demo, we just use the first device
    # device = device_list[0]
    controller = AdbController(
        adb_path=os.path.realpath('bin/platform-tools/adb.exe'),
        address="127.0.0.1:5555",
    )
    await controller.connect()

    maa_inst = Instance()
    maa_inst.bind(resource, controller)

    if not maa_inst.inited:
        print("Failed to init MAA.")
        exit()

    maa_inst.register_recognizer("MyRec", my_rec)
    maa_inst.register_action("MyAct", my_act)
    print("初始化完成")
    print(await maa_inst.run_task("Flag_NoButton1", {"Flag_NoButton1": {"recognition": "OCR",
                                                                        "text": "自动", "action": "Custom",
                                                                        "custom_action": "MyAct"}}))
    print("ok")


class MyRecognizer(CustomRecognizer):
    def analyze(
            self, context, image, task_name, custom_param
    ) -> Tuple[bool, RectType, str]:
        return True, (0, 0, 100, 100), "Hello World!"


class MyAction(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print(context, task_name, custom_param, box, rec_detail)
        return True

    def stop(self) -> None:
        pass


my_rec = MyRecognizer()
my_act = MyAction()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e,"出来了")
        # os.system('TASKKILL /F /IM  HD-Adb.exe /T')
        # os.kill(os.getpid(), signal.SIGTERM)

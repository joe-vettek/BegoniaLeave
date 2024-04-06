import json
import os.path
from typing import Tuple
import sys
sys.path.append(os.getcwd())
from bin.mfw.maa.define import RectType
from bin.mfw.maa.library import Library
from bin.mfw.maa.resource import Resource
from bin.mfw.maa.controller import AdbController
from bin.mfw.maa.instance import Instance
from bin.mfw.maa.toolkit import Toolkit, AdbDevice

from bin.mfw.maa.custom_recognizer import CustomRecognizer
from bin.mfw.maa.custom_action import CustomAction

import asyncio


async def main():
    version = Library.open("bin/mfw/bin")
    print(f"MaaFw Version: {version}")

    Toolkit.init_config()

    resource = Resource()

    await resource.load("asset/mfw/resource")

    device_cache = 'cache/device'
    print(11)
    if not os.path.exists(device_cache):
        device_list = await Toolkit.adb_devices()
        with open(device_cache, 'w') as file:
            txt = json.dumps([{"adb_path": str(device.adb_path),
                               "address": device.address} for device in device_list])
            print(txt)
            file.write(txt)
    else:
        with open(device_cache, 'r') as file:
            device_list = [ AdbDevice(adb_path=i["adb_path"],address=i["address"],name=None,controller_type=None,config=None) for i in json.loads(file.read())]

    # print(device_list)
    if not device_list:
        print("No ADB device found.")
        exit()

    # for demo, we just use the first device
    device = device_list[0]
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
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
                                                                        "text": "白夜极光", "action": "Custom",
                                                                        "custom_action": "MyAct"}}))


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
    asyncio.run(main())

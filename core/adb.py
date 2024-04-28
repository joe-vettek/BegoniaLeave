import datetime
import os
import random
import subprocess
import time
from typing import Union

import adbutils
import uiautomator2 as u2

from core import file_locator, screen_locator, log, config \
    # , _screen_locator as screen_locator

package_name = "com.tencent.baiye"


def sub_run(s):
    result = subprocess.run(s, shell=True, stdout=subprocess.PIPE, text=True)
    return result.stdout.split('\n')


def set_encoding():
    sub_run('chcp 65001')


def connect(need_killer=False):
    if need_killer:
        print(''.join(sub_run(file_locator.get_adb_name() + '  kill-server')))
    print(''.join(sub_run(file_locator.get_adb_name() + ' connect 127.0.0.1:5037')))


def get_device_auto():
    lines = sub_run(file_locator.get_adb_name() + " devices")
    for i, line in enumerate(lines):
        if line.endswith('device'):
            return line.split('device')[0].strip()


def decorate(specific=True, **kwargs):
    adb_cmd = file_locator.get_adb_name()
    if specific:
        adb_cmd += " -s " + get_device_auto()
    for i in kwargs:
        print(i, kwargs[i])
    return adb_cmd


def get_main_activity(package_name):
    cmd = decorate() + f' shell dumpsys package {package_name}'
    lines = sub_run(cmd)
    for i, line in enumerate(lines):
        if 'android.intent.action.MAIN:' in line or 'android.intent.category.LAUNCHER' in line:
            line = lines[i + 1]
            start = line.find(package_name)
            end = line.find(' ', start)
            return line[start:end]
    return None


def update_screenshot():
    # if os.path.exists('screen.png'):
    #     os.remove('screen.png')
    print(datetime.datetime.now())
    # sub_run(decorate() + ' shell screencap -p /sdcard/screen.png')
    # sub_run(decorate() + ' pull /sdcard/screen.png')
    # sub_run(decorate() + ' shell rm -r /sdcard/screen.png')
    sub_run(decorate() + '  exec-out screencap -p > cache/sc.png')
    print(datetime.datetime.now())


# print(set_encoding(),get_device_auto())
class AdbConnector:
    device: u2.Device

    def __init__(self):
        self.screenshot_take = None
        # try:
        #     self.device = u2.connect_usb(self.set_device())
        # except:
        #     # 目前这个检测有点问题
        #     self.device = u2.connect_adb_wifi("127.0.0.1:5555")
        self.device = u2.connect_adb_wifi(config.adb_path)
        self.device.__init__(config.adb_path)



    def set_device(self):
        holder = adbutils.AdbClient(host="127.0.0.1", port=5037)
        if len(holder.device_list()) > 0:
            return holder.device_list()[0].get_serialno()
        holder.disconnect("127.0.0.1:5037")

    def get_main_activity(self):
        return self.device.app_info(package_name)["mainActivity"]

    # 现在不再需要
    def restart(self):
        self.device.app_stop(package_name)
        self.device.app_start(package_name)

    def update_screenshot(self):
        if self.device:
            self.screenshot_take = self.device.screenshot(format="opencv")
            # self.screenshot_take.save(file_locator.get_cache_screenshot())
            # self.screenshot_take = screen_locator.read_img(file_locator.get_cache_screenshot())
            return self.screenshot_take
        else:
            print("Not valid device, can not update screenshot")

    def exists(self, template: str, update=True):
        if update:
            self.update_screenshot()
        location = screen_locator.ImageMatchInScreen(self.screenshot_take, screen_locator.read_img(template))
        if location:
            return True
        else:
            return False

    def exists_txt(self, txt: str, update=True,roi=None):
        if update:
            self.update_screenshot()
        location = screen_locator.text_center(self.screenshot_take, text_filter=txt,roi=roi)
        if location is not None and len(location) > 0:
            return True
        else:
            return False

    def if_exists(self, template: str, update=True):
        if update:
            self.update_screenshot()
        location = screen_locator.ImageMatchInScreenMult(self.screenshot_take, screen_locator.read_img(template))
        if location:
            return location
        else:
            return None

    def click_if_exists(self, template: str, reverse=True, double=False, delay: Union[float, int] = 0):
        if locations := self.if_exists(template):
            if len(locations) > 0:
                pos = locations[0] if not reverse else locations[-1]
                if delay > 0:
                    time.sleep(delay)
                self.click(pos[0], pos[1], double=double)
                return True
        return False

    def click_txt_if_exists(self, txt: str, reverse=True, double=False, delay: Union[float, int] = 0,roi=None):
        if locations := screen_locator.text_center(target=self.update_screenshot(), text_filter=txt,roi=roi):
            if locations is not None and len(locations) > 0:
                pos = locations[0] if not reverse else locations[-1][0]
                if delay > 0:
                    time.sleep(delay)
                self.click(pos[0], pos[1], double=double)
                return True
        return False

    def click(self, x: Union[float, int], y: Union[float, int], random_use=False, random_range=20, double=False,
              duration=0.5):
        if random_use:
            x = x + int(random_range * random.random())
            y = y + int(random_range * random.random())
        if config.log_click():
            log.printLog("点击 {} {}".format(x, y))
        if not double:
            self.device.click(x, y)
        else:
            self.device.double_click(x, y, duration * random.random())

    def drag(self, sx, sy, ex, ey, duration=0.5, random_use=False, random_range=20):
        if random_use:
            sx = sx + int(random_range * random.random())
            sy = sy + int(random_range * random.random())
            ex = ex + int(random_range * random.random())
            ey = ey + int(random_range * random.random())
        self.device.drag(sx, sy, ex, ey, duration)
        time.sleep(duration + random.random())


p_config = {'packageName': 'com.tencent.baiye', 'mainActivity': 'com.tencent.baiye.MainActivity', 'label': '白夜极光',
            'versionName': '1.13.0', 'versionCode': 2185136, 'size': 2076082511}
# 这里修改一下adb地址
os.environ["ADBUTILS_ADB_PATH"] = file_locator.get_adb_name()

import asyncio
import time

import numpy as np

from core import work_flow, utils, log, streamlist, screen_locator

click_list = ["N" for i in np.arange(4, 11, 1)]


# 第一个函数，这里等待重启
def auto_battle(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("开始做活动")
    while click_list:
        tet = click_list.pop()
        utils.random_sleep()
        utils.create_limited_action(lambda: work_holder.click_txt_if_exists(tet), 10, 0.5)
        start_battel(work_holder)
    utils.waiting_loading_txt(work_holder, "返回")

    log.printLog("结束战斗")


def start_battel(work_holder: work_flow.WorkFlow):
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("挑战关卡"), 10, 0.5)
    utils.random_sleep(extra_time=0.5)
    if work_holder.click_txt_if_exists("跳过"):
        utils.random_sleep(extra_time=0.5)
        work_holder.click_txt_if_exists("确认")
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("开始战斗"), 10, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("自动战斗"), 10, 0.5)
    utils.random_sleep()
    utils.waiting_loading_txt(work_holder, "战斗结果", interval=12)
    work_holder.click(100, 100, random_use=True, random_range=80)
    utils.random_sleep(3)


# asyncio.run(screen_locator.init_instance())
# 测试代码
# a = work_flow.WorkFlow()
#
# auto_battle(a)
#
# a.register_task(auto_battle)
# a.start()

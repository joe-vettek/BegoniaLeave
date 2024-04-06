import time

from core import work_flow, utils, log, streamlist, screen_locator


# 第一个函数，这里等待重启
def auto_battle(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("开始荒典")

    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("探索"), 10, 0.5)
    utils.random_sleep()
    utils.waiting_loading_txt(work_holder, "尖塔挑战")
    utils.random_sleep(0.5)
    log.printLog("尝试进行活动")
    # utils.create_limited_action(lambda: work_holder.click_txt_if_exists("荒典"), 10, 0.5)
    # 由于荒典不存在，这里取中间
    a = screen_locator.text_center(work_holder.update_screenshot(), text_filter=["尖塔挑战", "启迪互联"])
    work_holder.click((a[0][0][0] + a[1][0][0]) / 2, a[0][0][1])
    utils.random_sleep(extra_time=4)
    log.printLog("尝试进行挑战")
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("挑战"), 10, 0.5)
    utils.random_sleep(extra_time=0.5)
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("快速编队"), 10, 0.5)
    utils.random_sleep(extra_time=0.5)
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("清空选择"), 10, 0.5)
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("属性"), 10, 0.5)
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("属性"), 10, 0.5)
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("属性"), 10, 0.5)
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("属性"), 10, 0.5)
    work_holder.click(133,168,random_use=True)
    work_holder.click(320,168,random_use=True)
    work_holder.click(500,168,random_use=True)
    work_holder.click(750,168,random_use=True)
    work_holder.click(920,168,random_use=True)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("确定"), 10, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("开始战斗"), 10, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("自动"), 10, 0.5)
    utils.random_sleep(extra_time=60)
    utils.waiting_loading_txt(work_holder, "战斗结果", interval=20)
    utils.random_sleep(1.5)
    work_holder.click(100, 100, random_use=True, random_range=80)
    utils.random_sleep(3)
    utils.waiting_loading_txt(work_holder, "返回")
    log.printLog("结束战斗")


# 测试代码
# a = work_flow.WorkFlow()
# a.update_screenshot()
#
# auto_battle(a)

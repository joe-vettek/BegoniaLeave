import time

from core import work_flow, utils, log, streamlist


# 第一个函数，这里等待重启
def auto_battle(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("开始做活动")

    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("活动合聚"), 10, 0.5)
    utils.random_sleep()
    utils.waiting_loading_txt(work_holder, "返回")
    utils.random_sleep(0.5)
    log.printLog("尝试进行活动")
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("别动战术训练营"), 10, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("开始挑战"), 10, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("开始战斗"), 10, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_txt_if_exists("自动战斗"), 10, 0.5)
    utils.random_sleep()
    utils.waiting_loading_txt(work_holder, "战斗结果", interval=12)
    work_holder.click(100, 100, random_use=True, random_range=80)
    utils.random_sleep(3)
    utils.waiting_loading_txt(work_holder, "返回")
    log.printLog("结束战斗")


# 测试代码
# a = work_flow.WorkFlow()
#
# a.register_task(auto_battle)
# a.start()



import time

from core import work_flow, streamlist, utils, log


# 第一个函数，这里等待重启
def clear_energy(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("准备战斗")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIN_BATTLE), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BATTLE_COMMON), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BATTLE_COMMON_EXPERIENCE), 6, 0.5)
    utils.random_sleep()
    # 目前不做选关
    time.sleep(1)
    # 这个滑动属于没办法，当然也可以后续做检测，不过目前没必要
    for i in range(3):
        work_holder.drag(640,500,641,100,0.5,random_use=True)
    log.printLog("进行自动扫荡")
    utils.random_sleep(extra_time=1)
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BATTLE_AUTO), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BATTLE_AUTO_BUTTON_MAX_COUNT), 6,
                                0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BATTLE_AUTO_BUTTON_START), 6, 0.5)
    utils.waiting_loading(work_holder, streamlist.IMAGE_BATTLE_AUTO_COMPLETE)
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BATTLE_AUTO_COMPLETE), 6, 0.5)
    log.printLog("扫荡完成，正在准备返回桌面")
    utils.random_sleep()
    time.sleep(1)
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_COMMON_HOME), 15, 0.5)
    time.sleep(1)


# # 测试代码
# a = work_flow.WorkFlow()
#
# a.register_task(clear_energy)
# a.start()

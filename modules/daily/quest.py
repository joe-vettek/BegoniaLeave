import time

from core import work_flow, streamlist, utils, log


# 第一个函数，这里等待重启
def submit_mission(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("准备提交任务")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIN_QUEST), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_QUEST_COMPLETE), 6, 0.5)
    utils.random_sleep()
    utils.deal_with_get_item(work_holder)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_QUEST_BONUS), 6, 0.5)
    utils.random_sleep()
    # 这里领取有两页
    utils.deal_with_get_item(work_holder)
    utils.deal_with_get_item(work_holder)

    utils.waiting_loading(work_holder, streamlist.IMAGE_QUEST_HOME, 3)
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_QUEST_HOME), 5, 0.5)


# 测试代码
# a = work_flow.WorkFlow()
#
# a.register_task(submit_mission)
# a.start()


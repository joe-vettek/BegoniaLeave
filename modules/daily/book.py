import time

from core import work_flow, streamlist, utils, log


# 第一个函数，这里等待重启
def submit_book_mission(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("准备提交通行证任务")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIN_BOOK), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BOOK_QUEST), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BOOK_QUEST_COMPLETE), 6, 0.5)
    utils.random_sleep()
    utils.collect_mul_items(work_holder)
    utils.random_sleep()

    utils.waiting_loading(work_holder, streamlist.IMAGE_BOOK_HOME, 3)
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BOOK_HOME), 5, 0.5)


# 测试代码
# a = work_flow.WorkFlow()
#
# a.register_task(submit_book_mission)
# a.start()


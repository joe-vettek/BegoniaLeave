import time

from core import work_flow, streamlist, utils, log


# 第一个函数，这里等待重启
def receive_mail(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("访问邮箱")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIN_MAIL), 10, 0.5)
    utils.random_sleep()
    time.sleep(1)
    log.printLog("尝试收取所有邮件")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIL_RECEIVE_ALL_LIGHT), 10, 0.5)
    utils.random_sleep()
    # Todo:这里目前可能有bug，超多物品有领取问题
    utils.deal_with_get_item(work_holder)
    utils.deal_with_get_item(work_holder)
    utils.deal_with_get_item(work_holder)
    utils.deal_with_get_item(work_holder)
    log.printLog("返回主页")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_COMMON_HOME), 15, 0.5)

# 测试代码
# a = work_flow.WorkFlow()
#
# a.register_task(receive_mail)
# a.start()

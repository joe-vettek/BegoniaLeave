import time

from core import work_flow, streamlist, utils, log, screen_locator


# 第一个函数，这里等待重启
def restart_game(work_holder: work_flow.WorkFlow):
    is_home = utils.is_ui_home(work_holder.update_screenshot())
    # print(screen_locator.text_center(None, text_filter="白夜极光"))
    if not is_home:
        work_holder.restart()
        log.printLog("正在重启")
        utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_LOGIN_BUTTON), 300, 3)
        log.printLog("正在登录中")
        time.sleep(3)
        utils.create_limited_action(lambda: is_in_main(work_holder), 120, 0.5)
        log.printLog("登录完成")
    else:
        log.printLog("当前正在主界面")


# 为什么要写这个函数呢，因为登录之后会出来一大堆弹窗，我们需要依次退出或领取
# 首先确认是否已经到达主界面，如果没有，依次检测，如果哪一个都没有就等待
def is_in_main(work_holder: work_flow.WorkFlow):
    is_home = utils.is_ui_home(work_holder.update_screenshot())

    if not is_home:
        if work_holder.click_if_exists(streamlist.IMAGE_LOGIN_EXIT_BANNER):
            log.printLog("已关闭活动通知")
            utils.random_sleep(extra_time=1)
        # 后期拆分
        if work_holder.if_exists(streamlist.IMAGE_COMMON_HINT_GET_ITEMS):
            work_holder.click(600, 50, random_use=True)
            utils.random_sleep()
            return False
        if work_holder.if_exists(streamlist.IMAGE_LOGIN_EXIT_SIGN_ACTIVITY):
            log.printLog("发现签到活动")
            if work_holder.click_if_exists(streamlist.IMAGE_COMMON_CAN_GET):
                log.printLog("完成签到")
                return False
            if work_holder.click_if_exists(streamlist.IMAGE_LOGIN_EXIT_SIGN_ACTIVITY):
                utils.random_sleep()
        # 月度签到
        if work_holder.click_if_exists(streamlist.IMAGE_LOGIN_EXIT_SIGN_MONTH):
            print("完成月度签到")
            utils.random_sleep(extra_time=1.5)
    return is_home

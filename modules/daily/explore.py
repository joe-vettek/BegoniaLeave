import time

from core import work_flow, streamlist, utils, log


# 第一个函数，这里等待重启
def harvest_and_explore(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("访问巨像")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIN_COLOSSUS), 10, 0.5)

    utils.waiting_loading(work_holder, streamlist.IMAGE_FOUNDATION_EXPLORE)

    if work_holder.if_exists(streamlist.IMAGE_FOUNDATION_BONUS):
        log.printLog("正在领取奖励")
        utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_FOUNDATION_BONUS))
        utils.waiting_loading(work_holder, streamlist.IMAGE_FOUNDATION_EXPLORE)
        utils.random_sleep()
        if utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_FOUNDATION_BONUS_1), 2,
                                       0.5):
            # 尝试收取奖励1
            utils.collect_mul_items(work_holder)
        # 精度不够
        if utils.create_limited_action(
                lambda: work_holder.click_if_exists(streamlist.IMAGE_FOUNDATION_BONUS_2, double=True), 2,
                0.5):
            utils.collect_mul_items(work_holder)
        utils.random_sleep()
        if work_holder.exists(streamlist.IMAGE_FOUNDATION_BONUS_HINT):
            log.printLog("检测到入住升级提示，请手动完成，否则不能一键收集")
            work_holder.click(100, 100, random_use=True)
            utils.random_sleep(extra_time=0.5)

    log.printLog("正在前往探险")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_FOUNDATION_EXPLORE))
    utils.random_sleep(1.5,extra_time=1.5)

    # 假如需要领取东西的话，多检查几次
    log.printLog("检查是否有探险完成")
    if utils.waiting_loading(work_holder,streamlist.IMAGE_FOUNDATION_EXPLORE_COMPLETE,3):
        utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_FOUNDATION_EXPLORE_COMPLETE),
                                    5, 1)
        utils.collect_mul_items(work_holder)
        log.printLog("完成旧物品领取")
    else:
        log.printLog("无探险奖励可领取")

    log.printLog("准备探险")
    utils.random_sleep()
    explore_items = [streamlist.IMAGE_FOUNDATION_EXPLORE_STAR_6,
                     streamlist.IMAGE_FOUNDATION_EXPLORE_STAR_5,
                     streamlist.IMAGE_FOUNDATION_EXPLORE_STAR_4,
                     streamlist.IMAGE_FOUNDATION_EXPLORE_STAR_3]
    while not work_holder.exists(streamlist.IMAGE_FOUNDATION_EXPLORE_ENOUGH) and not work_holder.exists(
            streamlist.IMAGE_FOUNDATION_EXPLORE_ENOUGH_2):
        for item in explore_items:
            if work_holder.if_exists(item):
                work_holder.click_if_exists(item)
                utils.create_limited_action(
                    lambda: work_holder.click_if_exists(streamlist.IMAGE_FOUNDATION_EXPLORE_AUTO))
                utils.random_sleep(0.5)
                utils.create_limited_action(
                    lambda: work_holder.click_if_exists(streamlist.IMAGE_FOUNDATION_EXPLORE_CONFIRM))
                utils.random_sleep(0.5)
                break
                
        utils.random_sleep(0.5)
    log.printLog("准备返回主界面")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_COMMON_HOME))
    utils.waiting_loading(work_holder, streamlist.IMAGE_SHOP_HOME, 5)


# 测试代码
# a = work_flow.WorkFlow()
# a.update_screenshot()
# a.register_task(harvest_and_explore)
# a.start()
# work_holder = work_flow.WorkFlow()
# print(a.exists(streamlist.IMAGE_FOUNDATION_EXPLORE_ENOUGH), a.exists(streamlist.IMAGE_FOUNDATION_EXPLORE_ENOUGH_2,update=False))
# print(a.exists(streamlist.IMAGE_FOUNDATION_EXPLORE_ENOUGH_2))
# print(a.exists(streamlist.IMAGE_FOUNDATION_BONUS_1))
# print(a.click_if_exists(streamlist.IMAGE_FOUNDATION_BONUS_2,double=True),a.click_if_exists(streamlist.IMAGE_FOUNDATION_BONUS_2))

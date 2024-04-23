import time

from core import work_flow, streamlist, utils, log, config


# 第一个函数，这里等待重启
def clear_energy(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("准备战斗")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIN_BATTLE), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_BATTLE_COMMON), 6, 0.5)
    utils.random_sleep()
    battle_type = streamlist.IMAGE_BATTLE_COMMON_GOLD
    if config.update["daily"]["battle"] == "金币":
        pass
    elif config.update["daily"]["battle"] == "装备经验":
        battle_type = streamlist.IMAGE_BATTLE_COMMON_EXPERIENCE_EQUIPMENT
    elif config.update["daily"]["battle"].startswith("经验-"):
        battle_type = streamlist.IMAGE_BATTLE_COMMON_EXPERIENCE
    utils.create_limited_action(lambda: work_holder.click_if_exists(battle_type), 6, 0.5)
    utils.random_sleep()
    # 目前不做选关
    utils.random_sleep(extra_time=1.5)
    if config.update["daily"]["battle"].startswith("经验-"):
        if config.update["daily"]["battle"] == "经验-水":
            pass
        if config.update["daily"]["battle"] == "经验-火":
            work_holder.click(270, 300, random_use=True)
        if config.update["daily"]["battle"] == "经验-森":
            work_holder.click(270, 420, random_use=True)
        if config.update["daily"]["battle"] == "经验-雷":
            work_holder.click(270, 570, random_use=True)
    log.printLog(f'选择关卡:{config.update["daily"]["battle"]}')
    utils.random_sleep()
    # 这个滑动属于没办法，当然也可以后续做检测，不过目前没必要
    utils.delay_checker(lambda: work_holder.drag(640, 500, 641, 100, 0.5, random_use=True),
                        lambda: work_holder.exists_txt("等级5",roi=[468, 120, 136, 437]))
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

# print(a.exists_txt("等级5",roi=[457, 123, 150, 519]))
#
# a.register_task(clear_energy)
# a.start()
# a = work_flow.WorkFlow()
#
# utils.delay_checker(lambda: a.drag(640, 500, 641, 100, 0.5, random_use=True),
#                     lambda: a.exists_txt("等级5"))

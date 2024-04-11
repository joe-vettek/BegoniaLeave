import time

from core import work_flow, streamlist, utils, log,screen_locator


# 第一个函数，这里等待重启
def buy_random(work_holder: work_flow.WorkFlow):
    utils.ensure_ui_home(work_holder)
    log.printLog("准备随机购物")
    utils.waiting_loading(work_holder,streamlist.IMAGE_MAIN_SHOP)
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_MAIN_SHOP), 6, 0.5)
    utils.random_sleep()
    utils.waiting_loading(work_holder,streamlist.IMAGE_SHOP_HOME)
    # 这个滑动属于没办法，当然也可以后续做检测，不过目前没必要
    for i in range(1):
        work_holder.drag(60, 500, 80, 200, 0.5,random_range=True)
    time.sleep(1)
    utils.random_sleep()
    log.printLog("进行购物")
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_SHOP_GOLD_SHOP), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_SHOP_GOLD_ICON_LIGHT,reverse=True), 6, 0.5)
    utils.random_sleep()
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_SHOP_PURCHASE), 6, 0.5)
    utils.random_sleep()
    utils.collect_mul_items(work_holder)
    utils.waiting_loading(work_holder, streamlist.IMAGE_SHOP_HOME, 3)
    utils.create_limited_action(lambda: work_holder.click_if_exists(streamlist.IMAGE_SHOP_HOME), 5, 0.5)


# 测试代码
# a = work_flow.WorkFlow()
# a.update_screenshot()
#
# # a.register_task(buy_random)
# # a.start()
# print(a.exists(streamlist.IMAGE_SHOP_GOLD_ICON_LIGHT))
# print(screen_locator.ImageMatchInScreenMult(a.update_screenshot(),screen_locator.read_img(streamlist.IMAGE_SHOP_PURCHASE)))
# # utils.create_limited_action(lambda: a.click_if_exists(streamlist.IMAGE_SHOP_GOLD_ICON_LIGHT), 6, 0.5)
# a.click_if_exists(streamlist.IMAGE_SHOP_GOLD_ICON_LIGHT)
# screen_locator.run_check(a.update_screenshot(),screen_locator.read_img(streamlist.IMAGE_SHOP_GOLD_ICON_LIGHT))
# a=None
import os.path
import random
import time
from typing import Union

from core import work_flow, screen_locator, streamlist, log


def test_time(func):
    def wrapper(*agrs):
        start = time.time()
        result = func(*agrs)
        end = time.time()
        print(f"执行时间: {end - start}")
        return result

    return wrapper


def create_limited_action(fun, timeout=12, interval=0.5):
    b = work_flow.WaitWorkRunner(timeout, interval)
    b.set_work(fun)
    return b.wait_until_max()


def is_ui_home(screenshot):
    return screen_locator.ImageMatchInScreen(screenshot,
                                             screen_locator.read_img(streamlist.IMAGE_MAIN_SHOP)) is not None \
        and screen_locator.ImageMatchInScreen(screenshot,
                                              screen_locator.read_img(streamlist.IMAGE_MAIN_SHOP)) is not None


# Todo:未来需要强制
def ensure_ui_home(work_holder: work_flow.WorkFlow):
    pass


# 后期再写，现在做流式工作
# def where_is_me(screenshot):


def random_sleep(max_time: Union[int, float] = 1.0, extra_time: Union[int, float] = 0):
    time.sleep(random.random() * max_time + extra_time)


# 这个点击太通用了，写个函数处理一下
def deal_with_get_item(work_holder: work_flow.WorkFlow):
    if waiting_loading(work_holder, streamlist.IMAGE_COMMON_HINT_GET_ITEMS, timeout=1):
        work_holder.click(600, 50, random_use=True)
        random_sleep()
        # return deal_with_get_item(work_holder)
    return True


# 过场有两个阶段，第一个阶段是等待加载，第二个阶段是等待结束
def waiting_loading(work_holder: work_flow.WorkFlow, img_key, timeout=-1):
    if not work_holder.exists(img_key):
        return create_limited_action(lambda: work_holder.exists(img_key), timeout, 0.5)
    return True


def waiting_loading_txt(work_holder: work_flow.WorkFlow, txt, timeout=-1, interval=1):
    if not work_holder.exists_txt(txt):
        return create_limited_action(lambda: work_holder.exists_txt(txt), timeout, interval)
    return True


def collect_mul_items(work_holder: work_flow.WorkFlow):
    random_sleep(extra_time=0.5)
    result = False
    while work_holder.exists(streamlist.IMAGE_COMMON_HINT_GET_ITEMS):
        work_holder.click(600, 50, random_use=True)
        random_sleep(extra_time=1)
        result = True
    return result

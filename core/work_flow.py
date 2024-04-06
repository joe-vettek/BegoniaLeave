import threading
import time
import traceback
from typing import List

from core import adb, log, i18n

FLAG_START = 0
FLAG_RUN = 1
FLAG_COMPLETE = 3
FLAG_ERROR = 5
FLAG_HINT_EXIT = 11


# 我们使用这个来处理多次的任务和固定时长的任务
class TimeoutChecker:
    def __init__(self, timeout, sleep_interval):
        self.timeout = timeout
        self.sleep_interval = sleep_interval
        self.time_cost = 0

    def check_if_timeout(self):
        if self.timeout > 0:
            self.time_cost += self.sleep_interval
            if self.time_cost > self.timeout:
                return True
        return False

    def update_timeout(self, timeout):
        self.time_cost = 0
        self.timeout = timeout

    def cancel_timeout_check(self):
        self.time_cost = 0
        self.timeout = -1


class InternalSimpleWork(threading.Thread):
    def __init__(self, target=None, timeout=-1, name="NoName"):
        super().__init__(target=target)
        self.run_flag = FLAG_START
        self.timeout = timeout
        self.name = name

    def start(self) -> None:
        super().start()
        self.run_flag = FLAG_RUN

    def run(self) -> None:
        log.printLog("Now run " + self.name)
        try:
            super().run()
            self.run_flag = FLAG_COMPLETE
            log.printLog("Now finish " + self.name)
        except:
            self.run_flag = FLAG_ERROR


class WorkFlow(threading.Thread, TimeoutChecker, adb.AdbConnector):
    run_task: InternalSimpleWork

    def __init__(self):
        # super().__init__()
        log.printLog(i18n.translate(i18n.KEY_LOG_INIT))
        threading.Thread.__init__(self)
        TimeoutChecker.__init__(self, -1, 0.1)
        adb.AdbConnector.__init__(self)
        self.screenshot_take = None
        self.run_flag = FLAG_RUN
        self.task_list = []
        log.printLog(i18n.translate(i18n.KEY_LOG_INIT_SUCCESS))

    def register_task(self, func, timeout=-1, name="NoName"):
        self.task_list.append(InternalSimpleWork(target=lambda: func(self), timeout=timeout, name=name))

    def is_on_valid_task(self):
        return hasattr(self, "run_task") and self.run_task is not None and self.run_task.run_flag == FLAG_RUN

    def run(self) -> None:
        while self.run_flag == FLAG_RUN:
            # print(self.getName())
            if self.run_flag == FLAG_RUN:
                if not self.is_on_valid_task() and len(self.task_list) > 0:
                    self.run_task = self.task_list.pop(0)
                    self.update_timeout(self.run_task.timeout)
                    self.run_task.start()
                if self.check_if_timeout():
                    self.run_task = None
                    self.cancel_timeout_check()
                # 这里已经设置了Flag，因此直接执行
                time.sleep(self.sleep_interval)
            elif self.run_flag == FLAG_HINT_EXIT:
                self.device = None
                self.run_flag = FLAG_COMPLETE
                break

    def notify_stop(self, func=None):
        self.run_flag = FLAG_HINT_EXIT
        if func:
            func()


class WaitWorkRunner(TimeoutChecker):
    def __init__(self, timeout, sleep_interval):
        super().__init__(timeout, sleep_interval)
        self.func = None
        self.run_flag = FLAG_START

    def set_work(self, func):
        self.func = func

    def is_valid_work(self):
        return self.func is not None

    def do_work(self):
        try:
            return self.func()
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def wait_until_max(self):
        self.run_flag = FLAG_RUN
        if self.is_valid_work():
            while not self.check_if_timeout():
                if self.do_work():
                    self.run_flag = FLAG_COMPLETE
                    return True
                time.sleep(self.sleep_interval)
        self.run_flag = FLAG_ERROR
        return False


# 为什么这里又有一个队列，这个队列是为了便于快速汇总当前可以使用的函数，用于展示，并在运行时提供给任务管理线程
class TaskRegisterHolder:
    def __init__(self, func, name="NoName", weight=1000):
        self.name = name
        self.func = func
        self.weight = weight

    def push(self):
        global registered_task_list
        registered_task_list.append(self)
        registered_task_list = sorted(registered_task_list, key=lambda holder: holder.weight)


registered_task_list: List[TaskRegisterHolder] = []

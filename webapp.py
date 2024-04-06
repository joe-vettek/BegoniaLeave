import asyncio
import logging
import os
import signal
import sys

from fastapi import FastAPI, BackgroundTasks
from uvicorn import Config, Server

# 注意这里有一些问题哦
sys.path.append(os.getcwd())
import ctypes
import os
from typing import List
import uvicorn

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import modules
from core import work_flow, log, screen_locator

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import logging


class Item(BaseModel):
    modules: List[str]


work_flow_holder: work_flow.WorkFlow = None
modules.init()


# 这里配置支持跨域访问的前端地址
# origins = [
#     "http://localhost",  # 带端口的
#     "http://127.0.0.1",  # 不带端口的
#     # "http://localhost:5500"
# ]


def set_none():
    global work_flow_holder
    work_flow_holder = None


app = FastAPI()

app.mount("/main", StaticFiles(directory="webapp"), name="main")

# 将配置挂在到app上
app.add_middleware(
    CORSMiddleware,
    # 这里配置允许跨域访问的前端地址
    allow_origins=["*"],
    # 跨域请求是否支持 cookie， 如果这里配置true，则allow_origins不能配置*
    allow_credentials=False,
    # 支持跨域的请求类型，可以单独配置get、post等，也可以直接使用通配符*表示支持所有
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=RedirectResponse)
async def main_html():
    return "/main/main.html"


@app.get("/info")
async def info():
    return {
        "app_name": "FastAPI框架学习",
        "app_version": "v0.0.1"
    }


@app.get("/api/{sign}")
async def connect(sign: str):
    if sign == "log":
        out = log.log_cache[:]
        log.log_cache.clear()
        return out
    return [sign]


tasks: List = None
loop = None


async def background_init(item):
    global work_flow_holder

    if not server.should_exit and screen_locator.maa_inst is None:
        global tasks, loop
        print(os.getpid(), os.getpid())
        tasks, loop = await screen_locator.init_instance()
    if not server.should_exit and work_flow_holder is None:
        work_flow_holder = work_flow.WorkFlow()
        work_flow_holder.start()
        for h in work_flow.registered_task_list:
            if h.name in item.modules:
                log.printLog(f"Register module {h.name}")
                work_flow_holder.register_task(h.func, name=h.name)


@app.post("/api/{sign}")
async def connect(sign: str, item: Item, background_tasks: BackgroundTasks):
    global work_flow_holder
    print(item)
    if sign == "connect":
        background_tasks.add_task(background_init, item)

    elif sign == "disconnect":
        log.printLog("正在停止工作流")
        if loop:
            try:
                loop.stop()
                loop.close()
            finally:
                pass
        if work_flow_holder:
            work_flow_holder.notify_stop(lambda: set_none())
            work_flow_holder = None
    return [sign, item]


@app.get("/close")
async def close():
    print("尝试卸载服务器")
    # app.on_event("shutdown")
    # os.system('TASKKILL /F /IM  python.exe /T')
    # os.kill(os.getppid(), signal.SIGTERM)
    # os.kill(os.getpid(), signal.SIGTERM)
    # return []
    server.force_exit = True
    server.should_exit = True
    # await server.shutdown()
    # return []


@app.on_event("shutdown")
async def shutdown_event():
    print("Performing clean shutdown...")
    screen_locator.cancel_instance()
    # global  loop
    # loop=None
    if loop:
        loop.stop()
        loop.close()
    # if tasks:
    #     for i in tasks:
    #         print(i.done())
    # loop.stop()
    #
    # loop.close()
    os.kill(os.getpid(), signal.SIGTERM)


UVICORN_LOGGING_CONFIG: dict = uvicorn.config.LOGGING_CONFIG


# UVICORN_LOGGING_CONFIG["filters"] = {"access": {"()":""}}


class EndpointFilter(logging.Filter):
    """Filter class to exclude specific endpoints from log entries."""

    def __init__(self, excluded_endpoints: List[str]) -> None:
        """
        Initialize the EndpointFilter class.

        Args:
            excluded_endpoints: A list of endpoints to be excluded from log entries.
        """
        super().__init__()
        self.excluded_endpoints = excluded_endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter out log entries for excluded endpoints.

        Args:
            record: The log record to be filtered.

        Returns:
            bool: True if the log entry should be included, False otherwise.
        """
        return record.args and len(record.args) >= 3 and record.args[2] not in self.excluded_endpoints


# Define excluded endpoints
excluded_endpoints = ["/api/log"]

# Add filter to the logger
logging.getLogger("uvicorn.access").addFilter(EndpointFilter(excluded_endpoints))

if __name__ == "__main__":
    # os.system(os.path.join(os.getcwd(), 'webapp/main.html'))
    print("正在启动，若未启动浏览器可手动访问 http://127.0.0.1:8000/")
    # os.system(r'start bin\tauri\flower.exe')
    port = 8000
    # webbrowser.open(f"http://127.0.0.1:{port}/")
    # p = BrowerProcess(port, name='leaves')
    # p.start()
    # , log_level='critical'
    # uvicorn.run(app, port=port, log_config=UVICORN_LOGGING_CONFIG)
    config = Config(app, port=port, log_config=UVICORN_LOGGING_CONFIG)
    server = Server(config=config)
    server.run()

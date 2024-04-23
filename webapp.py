import asyncio
import logging
import os
import signal
import sys

from fastapi import FastAPI, BackgroundTasks, Request
from uvicorn import Config, Server

# from core.config import EndpointFilter, excluded_endpoints

# 注意这里有一些问题哦
sys.path.append(os.getcwd())
import ctypes
import os
from typing import List, Any, Union
import uvicorn

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import modules
from core import work_flow, log, screen_locator, file_locator,config

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import logging


class Item(BaseModel):
    modules: Union[List[str], None] = None
    config: Union[dict, None] = None


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
    allow_origins=["http://localhost", "https://tauri.localhost", "http://127.0.0.1"],
    # 跨域请求是否支持 cookie， 如果这里配置true，则allow_origins不能配置*
    allow_credentials=False,
    # 支持跨域的请求类型，可以单独配置get、post等，也可以直接使用通配符*表示支持所有
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=RedirectResponse)
async def main_html(request: Request):
    # 这里检查一下来源
    client_ip = request.client.host
    request_url = request.url
    print({"client_ip": client_ip, "request_url": str(request_url)})
    return "/main/main.html"


@app.get("/info")
async def info():
    return {
        "app_name": "海棠叶自动化助手后台--基于FastAPI框架",
        "app_version": "v0.0.1"
    }


@app.get("/api/{sign}")
async def connect(sign: str):
    if sign == "log":
        out = log.log_cache[:]
        log.log_cache.clear()
        return out
    if sign == "status":
        out = {}
        if work_flow_holder and work_flow_holder.run_task:
            # and len(work_flow_holder.task_list) > 0 and work_flow_holder.run_flag == work_flow.FLAG_RUN
            out["code"] = 200
        return out
    if sign == "config":
        out = {"port": file_locator.load_json(file_locator.get_device())[0]["address"].split(":")[-1]}
        return out
    return [sign]


tasks: List = None
loop = None


async def background_init(item):
    global work_flow_holder

    if not server.should_exit and screen_locator.maa_inst is None:
        global tasks, loop
        # print(os.getpid(), os.getpid())
        tasks, loop = await screen_locator.init_instance()
    if not server.should_exit and work_flow_holder is None:
        work_flow_holder = work_flow.WorkFlow()
        work_flow_holder.start()
    if work_flow_holder:
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
    elif sign == "config":
        if item.config:
            out = {"address": f"127.0.0.1:{item.config['port']}"}
            file_locator.save_json(file_locator.get_device(), [out])
            screen_locator.adb_path = out["address"]
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


# Add filter to the logger
logging.getLogger("uvicorn.access").addFilter(config.EndpointFilter(config.excluded_endpoints))

if __name__ == "__main__":
    # os.system(os.path.join(os.getcwd(), 'webapp/main.html'))
    print(f"正在启动，若未启动浏览器可手动访问 http://127.0.0.1:{config.port()}/")
    # os.system(r'start bin\tauri\flower.exe')
    # port = 8000
    # webbrowser.open(f"http://127.0.0.1:{port}/")
    # p = BrowerProcess(port, name='leaves')
    # p.start()
    # , log_level='critical'
    # uvicorn.run(app, port=port, log_config=UVICORN_LOGGING_CONFIG)
    config = Config(app, port=config.port(), log_config=UVICORN_LOGGING_CONFIG)
    server = Server(config=config)
    server.run()

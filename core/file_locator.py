import json
import os
from os.path import normpath, join, dirname

from core import config

# 初始化root位置
root = os.getcwd()
while "core" not in os.listdir(root):
    root = dirname(root)


def init():
    if not os.path.exists(get_log_dir()):
        os.mkdir(get_log_dir())
    if not os.path.exists(get_cache_dir()):
        os.mkdir(get_cache_dir())


def get_root():
    return root


def get_cache_dir():
    cache_dir = join(get_root(), "cache")
    return normpath(cache_dir)


def get_cache_screenshot():
    return normpath(join(get_cache_dir(), "screen_now.png"))


def get_asset():
    asset_dir = join(get_root(), "asset")
    return normpath(asset_dir)


def get_log_dir():
    log_dir = join(get_root(), "logs")
    return normpath(log_dir)


def get_lang():
    return normpath(join(get_asset(), "lang", config.get_server() + ".json"))


def get_adb_name():
    return normpath(join(get_root(), 'bin/platform-tools/adb.exe'))


def get_device():
    device_path = normpath(join(get_cache_dir(), 'device'))
    if not os.path.exists(device_path):
        save_json(device_path, [{"address": "127.0.0.1:5555"}])
    return device_path

def get_update():
    update_path = normpath(join(get_cache_dir(), 'update'))
    if not os.path.exists(update_path):
        save_json(update_path,  {
            "daily": {
                "battle": "经验-森"
            }
        })
    return update_path

def get_mfw_bin():
    return normpath(join(get_root(), 'bin', 'mfw', 'bin'))


def get_mfw_res():
    return normpath(join(get_root(), 'asset', 'mfw', 'resource'))


def get_mfw_agent():
    return normpath(join(get_root(), 'bin', 'mfw', 'agent'))


def load_text(file, encode="utf-8"):
    with open(file, "r", encoding=encode) as f:
        return f.read()


def save_text(file, text: str, encode="utf-8"):
    with open(file, "w", encoding=encode) as f:
        f.write(text)
    return True


def load_json(file) -> dict:
    return json.loads(load_text(file))


def save_json(file, d):
    return save_text(file, json.dumps(d,ensure_ascii=False))


init()

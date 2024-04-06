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
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    return normpath(cache_dir)


def get_cache_screenshot():
    return normpath(join(get_cache_dir(), "screen_now.png"))


def get_asset():
    asset_dir = join(get_root(), "asset")
    return normpath(asset_dir)


def get_log_dir():
    log_dir = join(get_root(), "log")

    return normpath(log_dir)


def get_lang():
    return normpath(join(get_asset(), "lang", config.get_server() + ".json"))


def get_adb_name():
    return normpath(join(get_root(), 'bin/platform-tools/adb.exe'))


def load_text(file, encode="utf-8"):
    with open(file, "r", encoding=encode) as f:
        return f.read()


def load_json(file) -> dict:
    return json.loads(load_text(file))

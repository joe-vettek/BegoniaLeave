from core import file_locator, log, config


def translate(key: str):
    lang = file_locator.load_json(file_locator.get_lang())
    if lang.get(key) is not None:
        return lang[key]
    else:
        log.printLog('Not found key "{}" in {} lang file.'.format(key, config.get_server()))


# LOG
KEY_LOG_INIT = "log.init"
KEY_LOG_INIT_SUCCESS = "log.init_success"
import datetime
import os
import time

from core import file_locator as fg


def standardPath(pathText):
    result = ""
    if type(pathText) == list:
        for i in pathText:
            result += str(i) + "，"
        result = result[:-1]
    else:
        result = str(pathText)

    return result.strip().replace("//", "\\").replace("/", "\\").replace("'", "")


def betterNum(num):
    return ("0" + str(num) if int(num) < 10 else num)


logNow: str = None
log_cache = []


def printLog(logInfo, isError=False):
    logInfo = str(logInfo)
    print(logInfo)
    log_cache.append({
        f'{time.time()}': logInfo
    })
    i = datetime.datetime.now()
    with open(logNow, "a", encoding="utf-8") as f:
        logInfo = '[{}年{}月{}日 {}:{}:{}] '.format(i.year, betterNum(i.month), betterNum(i.day), betterNum(i.hour),
                                                    betterNum(i.minute), betterNum(i.second)) + logInfo + '\n'
        f.write(logInfo)
        f.close()



def printNew():
    i = datetime.datetime.now()
    times = 0
    global logNow
    logNow = fg.join(fg.get_log_dir(), "{}-{}-{}.log".format(i.year, betterNum(i.month), betterNum(i.day)))
    while os.path.exists(logNow):
        times += 1
        logNow = fg.join(fg.get_log_dir(),
                         "{}-{}-{}-{}.log".format(i.year, betterNum(i.month), betterNum(i.day), times))


printNew()

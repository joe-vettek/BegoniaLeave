import os.path
import re

import requests
import json
import zipfile

url = "https://api.github.com/repos/MaaXYZ/MaaFramework/actions/artifacts"
response = requests.get(url)
info = [i for i in json.loads(response.text)["artifacts"] if "win-x86" in i["name"]][0]
print(json.dumps(info))
# response = requests.get(info["archive_download_url"])
if not os.path.exists('cache'):
    os.mkdir('cache')
print(name := "cache/{}.zip".format(info["name"]))

if not os.path.exists(name):
    response = requests.get('https://github.com/MaaXYZ/MaaFramework/releases/download/v1.6.5/MAA-win-x86_64-v1.6.5.zip')
    with open(name, "wb") as file:
        file.write(response.content)

# try:
#     if input("是否删除" + os.path.realpath("bin/mfw") + "，是请输出1") == "1":
#         os.remove("bin/mfw")
# except PermissionError:
#     print("权限错误")

z = zipfile.ZipFile(name, 'r')
for i in z.namelist():

    path = None
    if i.startswith("binding/Python/maa/"):
        path = os.path.join("bin/mfw/maa", i.replace("binding/Python/maa/", ""))
    elif i.startswith("bin/"):
        path = os.path.join("bin/mfw/bin", i.replace("bin/", ""))
    if path:
        # path="bin/mfw"
        # path=os.path.normpath(path)
        # print(path,i)
        # z.extract(i,path)
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        if os.path.isdir(path):
            print(path)
            continue
        with open(path, 'wb') as file:
            file.write(z.read(i))
        if path.endswith(".py"):
            with open(path, 'r', encoding='utf-8') as f:
                instance_txt = f.read()
                pattern = r"json\.dumps\((task_param|param)\)"
                replacement = r"json.dumps(\1, ensure_ascii=False)"
                new_instance_txt = re.sub(pattern, replacement, instance_txt)
            if new_instance_txt != instance_txt:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_instance_txt)

# for i in z.namelist():
#
#     path = None
#     if i.startswith("binding/Python/maa/"):
#         path = os.path.join("bin/mfw/maa", i.replace("binding/Python/maa/", ""))
#     elif i.startswith("bin/"):
#         path = os.path.join("bin/mfw/bin", i.replace("bin/", ""))
#     if path:
#         z.extract(i, "bin/mfw")
#         try:
#             if os.path.normpath(os.path.join("bin/mfw", i)) != os.path.normpath(path):
#                 os.remove(path)
#                 os.rename(os.path.join("bin/mfw", i), path)
#         except:
#             print("创建和移动失败", i,'-->',path)
#         if not os.path.exists(os.path.dirname(path)):
#             os.mkdir(os.path.dirname(path))
#         if os.path.isdir(path):
#             print(path)
#             continue
#         with open(path, 'wb') as file:
#             file.write(z.read(i))
#         if path.endswith(".py"):
#             with open(path, 'r', encoding='utf-8') as f:
#                 instance_txt = f.read()
#                 # mfw1.6.5对中文传参有一定问题，需要修改代码
#                 pattern = r"json\.dumps\((task_param|param)\)"
#                 replacement = r"json.dumps(\1, ensure_ascii=False)"
#                 new_instance_txt = re.sub(pattern, replacement, instance_txt)
#             if new_instance_txt != instance_txt:
#                 with open(path, 'w', encoding='utf-8') as f:
#                     f.write(new_instance_txt)
#
# os.system('rd "{}"'.format(os.path.realpath('bin/mfw/binding/Python/maa')))
# os.system('rd "{}"'.format(os.path.realpath('bin/mfw/binding/Python')))
# os.system('rd "{}"'.format(os.path.realpath('bin/mfw/binding')))


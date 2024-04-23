import os.path
import re
import sys

import requests
import json
import zipfile


# url = "https://api.github.com/repos/MaaXYZ/MaaFramework/actions/artifacts"
# response = requests.get(url)
# info = [i for i in json.loads(response.text)["artifacts"] if "win-x86" in i["name"]][0]
# print(json.dumps(info))
def get_all_releases(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


repo_owner = "MaaXYZ"
repo_name = "MaaFramework"
all_releases = get_all_releases(repo_owner, repo_name)
as_list = all_releases[0]['assets']
zip_info = [i for i in as_list if 'win-x86_64' in i["name"]][0]

# print(zip_info)
# sys.exit(0)
# response = requests.get(info["archive_download_url"])
if not os.path.exists('cache'):
    os.mkdir('cache')
print(name := "cache/{}".format(zip_info["name"]))

if not os.path.exists(name):
    response = requests.get(zip_info["browser_download_url"])
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
    elif i.startswith("share/MaaAgentBinary"):
        path = os.path.join("bin/mfw/agent", i.replace("share/MaaAgentBinary/", ""))
    elif i.endswith('LICENSE.md'):
        path = os.path.join("bin/mfw", 'LICENSE.md')
    if path:
        # path="bin/mfw"
        # path=os.path.normpath(path)
        # print(path,i)
        # z.extract(i,path)
        # 也许会有更好的方法判断路径，但是由于我们目前的路径都是多层的
        # if not os.path.exists(os.path.dirname(path)):
        if path.endswith('/') or path.endswith('\\'):
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
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

for i in z.namelist():
    if i.startswith("tools/ImageCropper"):
        z.extract(i, "cache")


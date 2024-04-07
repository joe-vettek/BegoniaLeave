import os.path
import re

import requests
import json
import zipfile

url = "https://github.com/MaaXYZ/MaaFramework/refs?type=tag"
response = requests.get(url)
response=requests.get(r'https://github.com/MaaXYZ/MaaFramework/releases/expanded_assets/v1.7.0-alpha.3')
print(response.text,response.status_code)
# print(response.json())
# info = [i for i in json.loads(response.text)["artifacts"] if "win-x86" in i["name"]][0]
# print(json.dumps(info))
# response = requests.get(info["archive_download_url"])
# if not os.path.exists('cache'):
#     os.mkdir('cache')
# print(name := "cache/{}.zip".format(info["name"]))
#
# if not os.path.exists(name):
#     response = requests.get('https://github.com/MaaXYZ/MaaFramework/releases/download/v1.6.5/MAA-win-x86_64-v1.6.5.zip')
#     with open(name, "wb") as file:
#         file.write(response.content)




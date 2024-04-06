import os.path
import zipfile
import requests

if not os.path.exists('cache'):
    os.mkdir('cache')
print(name := "cache/{}.zip".format("platform-tools-latest-windows"))

if not os.path.exists(name):
    response = requests.get('https://dl.google.com/android/repository/platform-tools-latest-windows.zip?hl=zh-cn')
    with open(name, "wb") as file:
        file.write(response.content)

z = zipfile.ZipFile(name, 'r')
print(z.namelist())
z.extractall('bin')

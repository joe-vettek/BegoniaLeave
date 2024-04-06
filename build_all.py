import os
# import clear_cache
import shutil

# clear_cache.clean_cache()

need = []


def get_in(alle, path):
    for c in os.listdir(path):
        dc = os.path.join(path, c)
        if os.path.isdir(dc):
            get_in(alle, dc)
        else:
            if r'bin\python' not in dc and '__pycache__' not in dc and r'bin\mfw\bin\debug' not in dc and r'bin\mfw\bin\config' not in dc:
                alle.append(dc)
    return alle


def mk_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


import zipfile

# print(get_in([], 'bin'))
mk_dir('bin')
mk_dir(r'bin\tauri')
os.system('call ' + os.path.realpath('setup/build.bat'))
shutil.copy(r'setup\publish\BegoniaLeaveSetup.exe', 'bin\BegoniaLeaveSetup.exe')
os.system('call ' + os.path.realpath('flower/build.bat'))
shutil.copy(r'flower\src-tauri\target\release\flower.exe', r'flower.exe')
# 文件列表
files_to_zip = ['webapp.py', 'flower.exe', '安装.bat', '启动入口.bat']
files_to_zip.extend(get_in([], 'bin'))
files_to_zip.extend(get_in([], 'core'))
files_to_zip.extend(get_in([], 'modules'))
files_to_zip.extend(get_in([], 'asset'))
files_to_zip.extend(get_in([], 'webapp'))
# ZIP文件名
zip_filename = 'BegoniaLeave.zip'
files_to_zip = set(files_to_zip)
# 创建一个ZIP文件对象
with zipfile.ZipFile(zip_filename, 'w') as zip_obj:
    # 遍历所有文件，并将它们添加到ZIP文件中
    for file in files_to_zip:
        zip_obj.write(file)

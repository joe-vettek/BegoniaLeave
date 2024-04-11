import ctypes
import os.path

from core import  file_locator

path=os.path.join(file_locator.get_mfw_bin(),"fastdeploy_ppocr_maa.dll")
fastdeploy_ppocr = ctypes.WinDLL(path)
print(fastdeploy_ppocr.version)

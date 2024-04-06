
from core import screen_locator,file_locator,utils


img=screen_locator.read_img(file_locator.get_cache_screenshot())

text_centerresult=screen_locator.text_center(screen_locator.quick_screenshot(),text_filter="战斗结果")
print(text_centerresult)

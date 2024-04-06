from core import config, screen_locator, file_locator, work_flow

a = work_flow.WorkFlow()
a.update_screenshot()
screen_locator.run_check(screen_locator.read_img(file_locator.get_cache_screenshot()),screen_locator.read_img('blueBlock.png'))

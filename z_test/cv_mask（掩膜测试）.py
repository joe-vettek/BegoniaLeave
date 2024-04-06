from core import config, screen_locator, file_locator, work_flow


screen_locator.run_check(screen_locator.read_img('s.jpg'),
                         screen_locator.read_img('mask-2.jpg'),
                         mask=screen_locator.read_img('mask-2.jpg'))

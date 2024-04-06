import asyncio

from core import screen_locator


asyncio.run(screen_locator.init_instance())
print(screen_locator.text_center(None, text_filter="应用"))
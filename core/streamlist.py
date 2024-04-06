import os.path
import sys

from core import config
from core import file_locator


# 根据设置的服务器类型加载资源
# local_cache=dir(this)
def init():
    mod = sys.modules[__name__]
    local_cache = dir(mod)
    for v in local_cache:
        if v.startswith("IMAGE"):
            old_v = getattr(mod, v)
            setattr(mod, v, get_image(old_v))


def get_image(path):
    return os.path.normpath(os.path.join(*[file_locator.get_asset(), config.get_server(), path]))


# BATTLE
IMAGE_BATTLE_AUTO = "battle/auto.png"
IMAGE_BATTLE_AUTO_BUTTON_MAX_COUNT = "battle/auto_button_max_count.png"
IMAGE_BATTLE_AUTO_BUTTON_START = "battle/auto_button_start.png"
IMAGE_BATTLE_AUTO_COMPLETE = "battle/auto_complete.png"
IMAGE_BATTLE_AUTO_COST_30 = "battle/auto_cost_30.png"
IMAGE_BATTLE_COMMON = "battle/common.png"
IMAGE_BATTLE_COMMON_EXPERIENCE = "battle/common_experience.png"
IMAGE_BATTLE_COMMON_EXPERIENCE_EQUIPMENT = "battle/common_experience_equipment.png"
IMAGE_BATTLE_COMMON_GOLD = "battle/common_gold.png"

# BOOK
IMAGE_BOOK_HOME = "book/home.png"
IMAGE_BOOK_QUEST = "book/quest.png"
IMAGE_BOOK_QUEST_COMPLETE = "book/quest_complete.png"

# COMMON
IMAGE_COMMON_CAN_GET = "common/can_get.png"
IMAGE_COMMON_HINT_GET_ITEMS = "common/hint_get_items.png"
IMAGE_COMMON_HOME = "common/home.png"
IMAGE_COMMON_LOADING = "common/loading.png"

# FOUNDATION
IMAGE_FOUNDATION_BONUS = "foundation/bonus.png"
IMAGE_FOUNDATION_BONUS_1 = "foundation/bonus_1.png"
IMAGE_FOUNDATION_BONUS_2 = "foundation/bonus_2.png"
IMAGE_FOUNDATION_BONUS_HINT = "foundation/bonus_hint.png"
IMAGE_FOUNDATION_EXPLORE = "foundation/explore.png"
IMAGE_FOUNDATION_EXPLORE_AUTO = "foundation/explore_auto.png"
IMAGE_FOUNDATION_EXPLORE_COMPLETE = "foundation/explore_complete.png"
IMAGE_FOUNDATION_EXPLORE_CONFIRM = "foundation/explore_confirm.png"
IMAGE_FOUNDATION_EXPLORE_ENOUGH = "foundation/explore_enough.png"
IMAGE_FOUNDATION_EXPLORE_ENOUGH_2 = "foundation/explore_enough_2.png"
IMAGE_FOUNDATION_EXPLORE_STAR_3 = "foundation/explore_star_3.png"
IMAGE_FOUNDATION_EXPLORE_STAR_4 = "foundation/explore_star_4.png"
IMAGE_FOUNDATION_EXPLORE_STAR_5 = "foundation/explore_star_5.png"
IMAGE_FOUNDATION_EXPLORE_STAR_6 = "foundation/explore_star_6.png"

# LOGIN
IMAGE_LOGIN_BUTTON = "login/button.png"
IMAGE_LOGIN_EXIT_BANNER = "login/exit_banner.png"
IMAGE_LOGIN_EXIT_SIGN_ACTIVITY = "login/exit_sign_activity.png"
IMAGE_LOGIN_EXIT_SIGN_MONTH = "login/exit_sign_month.png"
IMAGE_LOGIN_HINT = "login/hint.png"
IMAGE_LOGIN_QQ = "login/qq.png"

# MAIL
IMAGE_MAIL_RECEIVE_ALL_LIGHT = "mail/receive_all_light.png"

# MAIN
IMAGE_MAIN_BATTLE = "main/battle.png"
IMAGE_MAIN_BOOK = "main/book.png"
IMAGE_MAIN_COLOSSUS = "main/colossus.png"
IMAGE_MAIN_MAIL = "main/mail.png"
IMAGE_MAIN_QUEST = "main/quest.png"
IMAGE_MAIN_SHOP = "main/shop.png"

# QUEST
IMAGE_QUEST_BONUS = "quest/bonus.png"
IMAGE_QUEST_COMPLETE = "quest/complete.png"
IMAGE_QUEST_HOME = "quest/home.png"

# SHOP
IMAGE_SHOP_GOLD_ICON_LIGHT = "shop/gold_icon_light.png"
IMAGE_SHOP_GOLD_SHOP = "shop/gold_shop.png"
IMAGE_SHOP_HOME = "shop/home.png"
IMAGE_SHOP_PURCHASE = "shop/purchase.png"

init()

from core import work_flow
from modules.activity import huangdian
from modules.login import restart
from modules.daily import mail, explore, battle, book, shop, quest


# 这里注册的函数都不需要写参数，默认提供work_flow.WorkFlow作为输入
def init():
    work_flow.TaskRegisterHolder(login.restart.restart_game, weight=0, name="login-restart").push()

    work_flow.TaskRegisterHolder(mail.receive_mail, weight=100, name="daily-mail").push()
    work_flow.TaskRegisterHolder(explore.harvest_and_explore, weight=110, name="daily-explore").push()
    work_flow.TaskRegisterHolder(battle.clear_energy, weight=200, name="daily-battle").push()
    work_flow.TaskRegisterHolder(shop.buy_random, weight=300, name="daily-shop").push()
    work_flow.TaskRegisterHolder(quest.submit_mission, weight=1000, name="daily-quest").push()
    work_flow.TaskRegisterHolder(book.submit_book_mission, weight=2000, name="daily-book").push()

    work_flow.TaskRegisterHolder(huangdian.auto_battle, weight=500, name="battle-huangdian").push()
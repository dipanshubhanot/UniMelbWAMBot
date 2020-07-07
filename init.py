from WamBot import *
import sqlite3 as sql
from secret import Username
conn = sql.connect("wambase.db")

user = Username()
deepBot = WamBot(user.username, user.name, user.password)
deepBot.login()
deepBot.open_results()
sleep(5)
deepBot.open_recent_results()
deepBot.switch_wam_window()

while True:
    deepWAM = deepBot.check_wam()
    deepBot.store_wam(deepWAM)
    sleep(5)
    deepBot.driver.refresh()




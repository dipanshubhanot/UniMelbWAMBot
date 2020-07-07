from WamBot import *
import sqlite3 as sql
from secret import Username
conn = sql.connect("wambase.db")

# should be in number of seconds
TIME_BETWEEN_EACH_REFRESH = 15;
# should be in number of hours
TIME_BETWEEN_EACH_NOTIF = 0.5

# all fields are case sensitive
# Phone Number must be in the format:+61456789012
# Phone number must be entered without any spaces and with a country code
you = Username("userName", "Password", "Name", "Phone Number")
yourBot = WamBot(you.username,you.name,you.password,you.phone)

# lists to keep track of bot(s), last checked WAM and notification settings
bots = []
wams = []
counters =[]

bots.append(yourBot)

for bot in bots:
    bot.login()
    bot.open_results()
    sleep(3)
    bot.open_recent_results()
    bot.switch_wam_window()
    wams.append(bot.check_wam())
    client = Client()
    client.messages.create(body="Your current WAM is "+str(bot.check_wam()),
                           from_=bot.from_whatsapp_number,
                           to=bot.phonenum)
    counters.append(0)

while True:
    for i in range(len(bots)):
        thisWAM = bots[i].check_wam()
        bots[i].store_wam(thisWAM)
        counters[i] += 1
        if thisWAM != wams[i]:
            bots[i].send_notification(wams[i], thisWAM)
            counters[i] = 0
        if counters[i] >= TIME_BETWEEN_EACH_NOTIF*60*60/TIME_BETWEEN_EACH_REFRESH:
            bots[i].send_no_change_notif()
            counters[i] = 0
        wams[i] = thisWAM
        sleep(TIME_BETWEEN_EACH_REFRESH/len(bots))
        bots[i].driver.refresh()



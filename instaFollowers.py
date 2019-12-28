import instabot
import time

bot = instabot.Bot(filter_users=False)

bot.login(username="", password="")

ansList = bot.get_user_following(user_id=bot.get_user_id_from_username("rustinpieces_ftc15692"))

print(ansList)

unList = []

for val in ansList:
    newName = bot.get_username_from_user_id(val)
    unList.append(newName)
    print(newName)
    time.sleep(2)


print(unList)
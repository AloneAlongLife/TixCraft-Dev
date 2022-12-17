from bs4 import BeautifulSoup, Tag
from requests import session
from orjson import loads
from time import time_ns, sleep

sen = session()

# URL = "https://tixcraft.com/activity/game/23_ssf4"
# URL = "https://tixcraft.com/activity/game/23_wbc"
URL = "https://tixcraft.com/activity/game/23_goodband"
TICKS = 1

sen.cookies.set("SID", "48lpsjuko33o9jpt84hh870dai")

timer = time_ns()
print("timer_start")

while True:
    try:
        r = sen.get(URL)
        home_page: BeautifulSoup = BeautifulSoup(r.content, features="html.parser")
        game_url = home_page.select_one("#gameList input")["data-href"]
        break
    except:
        print(f"\r尚未開賣 {r.status_code} {time_ns() - timer}", end="")
        # sleep(0.05)
        continue

games: BeautifulSoup = BeautifulSoup(sen.get(f"https://tixcraft.com{game_url}").content, features="html.parser")
url_data = loads(games.decode().split("var areaUrlList = ")[1].split(";")[0].replace("\\", ""))

a_tag = games.select_one("div.zone.area-list a")
game_id = a_tag["id"]
print(f"取得: {a_tag.text}")

order_url = f"https://tixcraft.com{url_data[game_id]}"
order_page: BeautifulSoup = BeautifulSoup(sen.get(order_url).content, features="html.parser")

form: Tag = order_page.select_one("form")
agree = "TicketForm[agree]" + order_page.decode().split('\"name\", \"TicketForm[agree]')[1].split('\");')[0]

form_data = {
    "CSRFTOKEN": form.select_one("#CSRFTOKEN")["value"],
    agree: 1,
    "ticketPriceSubmit": ""
}

tick_list = form.select("#ticketPriceList select")
tick_list_2 = form.select("#ticketPriceList input")
form_data[tick_list[0]["name"]] = TICKS
form_data[tick_list_2[0]["name"]] = tick_list_2[0]["value"]

for i, tic in enumerate(tick_list[1:], 1):
    form_data[tic["name"]] = 0
    form_data[tick_list_2[i]["name"]] = tick_list_2[i]["value"]

open("out.png", mode="wb").write(sen.get("https://tixcraft.com/ticket/captcha").content)
form_data["TicketForm[verifyCode]"] = input("verifyCode:")

sen.post(order_url, data=form_data)
check_res = sen.get("https://tixcraft.com/ticket/check")

check_data = loads(check_res.content)
print(check_data["message"])
if check_data["waiting"]:
    sleep(check_data["time"])
    print("搶票成功 請前往該帳號訂單查看: https://tixcraft.com/order")
else:
    print(check_res.content)
    input("搶票失敗 按Enter鍵離開...")

print((time_ns() - timer) * 10**-9)
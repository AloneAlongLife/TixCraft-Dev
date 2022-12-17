from bs4 import BeautifulSoup, Tag
from requests import session, Session
from orjson import loads, JSONDecodeError
from time import time, sleep
from numpy import frombuffer, uint8
from cv2 import imdecode, IMREAD_COLOR, cvtColor, COLOR_BGR2GRAY, INTER_NEAREST, resize
from threading import Thread

def print_vcode(_sen: Session):
    for _ in range(3):
        out = []
        for _ in range(3):
            img = imdecode(frombuffer(_sen.get("https://tixcraft.com/ticket/captcha").content, uint8), IMREAD_COLOR)
            img = cvtColor(img, COLOR_BGR2GRAY)
            img = resize(img, (75, 60), interpolation=INTER_NEAREST)

            img[img < 250] = 0
            temp = img.astype("U2")
            temp[temp == "0"] = " "
            temp[temp != " "] = "#"
            temp = [l for l in temp.tolist() if "#" in l]
            out.append(temp)
        _p = "\n".join(map(lambda x: "|".join(map(lambda y: "".join(y), x)), zip(out[0], out[1], out[2])))
        print(_p)
        print("-" * 228)

URL = input("URL :")
if not URL: URL = "https://tixcraft.com/activity/game/23_ssf4"
# URL = "https://tixcraft.com/activity/game/23_wbc"
elif URL == "test": URL = "https://tixcraft.com/activity/game/23_goodband"

SID = input("SID: ")
if not SID: SID = "tr1ofvg0fmjrrsanm8nref8jda"

try: TICKS = int(input("Ticket Count: "))
except: TICKS = 1

sen = session()
sen.cookies.set("SID", SID)

timer = time()
while not (game_tag := (game_page := BeautifulSoup((r := sen.get(URL)).content, features="html.parser")).select_one("#gameList input")):
    print(f"\r{game_page.select_one('h2.activity-title').text} 尚未開賣 {r.status_code} {format(time() - timer, '.2f')}s", end="")

timer = time()
print("timer_start")

games: BeautifulSoup = BeautifulSoup(sen.get(f"https://tixcraft.com{game_tag['data-href']}").content, features="html.parser")
url_data = loads(games.decode().split("var areaUrlList = ")[1].split(";")[0].replace("\\", ""))

while True:
    a_tag = games.select_one("div.zone.area-list a")
    game_id = a_tag["id"]
    print(f"取得: {a_tag.text} t={time() - timer}")

    order_url = f"https://tixcraft.com{url_data[game_id]}"
    order_page: BeautifulSoup = BeautifulSoup(sen.get(order_url).content, features="html.parser")
    Thread(target=print_vcode, args=(sen,)).start()

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
    for tic, pic in zip(tick_list[1:], tick_list_2[1:]):
        form_data[tic["name"]] = 0
        form_data[pic["name"]] = pic["value"]

    # open("out.png", mode="wb").write(sen.get("https://tixcraft.com/ticket/captcha").content)
    form_data["TicketForm[verifyCode]"] = input("verifyCode:")

    sen.post(order_url, data=form_data)
    check_res = sen.get("https://tixcraft.com/ticket/check")

    try:
        check_data = loads(check_res.content)
    except JSONDecodeError:
        print("SID錯誤 請重新輸入")
        SID = input("SID: ")
        sen.cookies.set("SID", SID)
        continue
    print(check_data["message"])
    if check_data["waiting"]:
        # sleep(check_data["time"])
        print("搶票成功 請前往該帳號訂單查看: https://tixcraft.com/ticket/checkout")
        break
    else:
        print(check_res.content)
        print("搶票失敗 重新開始...")
        games: BeautifulSoup = BeautifulSoup(sen.get(f"https://tixcraft.com{game_tag['data-href']}").content, features="html.parser")

print((time() - timer))
input("End..")
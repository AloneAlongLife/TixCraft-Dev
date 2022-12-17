from bs4 import BeautifulSoup, Tag
from requests import session, Session
from orjson import loads, JSONDecodeError
from time import time, sleep
from numpy import frombuffer, uint8, full
from cv2 import imdecode, IMREAD_COLOR, cvtColor, COLOR_BGR2GRAY, INTER_NEAREST, resize
from threading import Thread, Lock
from webbrowser import get as w_get
from queue import Queue

def print_vcode(_sen: Session):
    def longer(inp: list):
        return inp + [" " * 75] * (max_h - len(inp))
    for _ in range(3):
        out = []
        for _ in range(3):
            img = imdecode(frombuffer(_sen.get("https://tixcraft.com/ticket/captcha").content, uint8), IMREAD_COLOR)
            img = resize(cvtColor(img, COLOR_BGR2GRAY), (75, 40), interpolation=INTER_NEAREST)

            temp = full(img.shape, " ")
            temp[img > 250] = "#"
            temp = [k for k in map("".join, temp.tolist()) if "#" in k]
            out.append(temp)
        max_h = max(map(len, out))
        out = tuple(map(longer, out))
        _p = "\n".join(map("|".join, zip(*out)))
        print(_p)
        print("-" * 228)

PRINT_QUEUE: Queue = Queue()
STARTED = False
STARTED_LOCK = Lock()
SLEEP_TIME = 0

URL = input("URL :")
if not URL: URL = "https://tixcraft.com/activity/game/23_ssf4"
# URL = "https://tixcraft.com/activity/game/23_wbc"
elif URL == "test": URL = "https://tixcraft.com/activity/game/23_goodband"

SID = input("SID :")
if not SID: SID = "tr1ofvg0fmjrrsanm8nref8jda"

try: TICKS = int(input("Ticket Count :"))
except: TICKS = 1

sen = session()
sen.cookies.set("SID", SID)

timer = time()
game_tag = None
def refresh_job():
    global game_tag, STARTED
    while not STARTED:
        if gt := (game_page := BeautifulSoup((r := sen.get(URL)).content, features="html.parser")).select_one("#gameList input"):
            STARTED_LOCK.acquire()
            if STARTED:
                STARTED_LOCK.release()
                return
            STARTED = True
            game_tag = gt
            STARTED_LOCK.release()
            return
        if STARTED: return
        try: PRINT_QUEUE.put(f"\r{game_page.select_one('h2.activity-title').text} 尚未開賣 {r.status_code} {format(time() - timer, '.2f')}s")
        except: PRINT_QUEUE.put(f"\rERROR {r.status_code} {format(time() - timer, '.2f')}s")
        sleep(SLEEP_TIME)
        if STARTED: return

try:
    for _ in range(1): Thread(target=refresh_job).start()
    _get_i = 0
    _timer_offset = timer
    while not STARTED:
        if PRINT_QUEUE.empty():
            sleep(0.001)
            continue
        _get_i += 1
        _rate = _get_i / max(0.001, time() - _timer_offset)
        if time() - _timer_offset > 2:
            # SLEEP_TIME = max(0, SLEEP_TIME + 0.01 * (_rate - 8))
            _get_i, _timer_offset = 0, time()
        print(f"{PRINT_QUEUE.get()} {format(_rate, '.2f')}r/s", end="")
except Exception as e:
    STARTED = True
    raise e

# _get_i = 0
# while not (game_tag := (game_page := BeautifulSoup((r := sen.get(URL)).content, features="html.parser")).select_one("#gameList input")):
#     _get_i += 1
#     try:
#         print(f"\r{game_page.select_one('h2.activity-title').text} 尚未開賣 {r.status_code} {format(time() - timer, '.2f')}s {format(_get_i / (time() - timer), '.2f')}r/s", end="")
#     except:
#         print(f"\r尚未開賣 {r.status_code} {format(time() - timer, '.2f')}s {format(_get_i / (time() - timer), '.2f')}r/s", end="")

timer = time()
print("timer_start")
while True:
    games: BeautifulSoup = BeautifulSoup(sen.get(f"https://tixcraft.com{game_tag['data-href']}").content, features="html.parser")
    try:
        url_data = loads(games.decode().split("var areaUrlList = ")[1].split(";")[0].replace("\\", ""))
        break
    except:
        continue

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
    form_data["TicketForm[verifyCode]"] = input("verifyCode:\n")

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
        for i in range(check_data["time"]):
            print(f"\r搶票成功 請等待{check_data['time'] - i}秒...", end="")
            sleep(1)
        print("\r搶票成功 請等待0秒... 請前往該帳號訂單查看: https://tixcraft.com/ticket/checkout")
        w_get("windows-default").open("https://tixcraft.com/ticket/checkout")
        break
    else:
        print(check_res.content)
        print("搶票失敗 重新開始...")
        games: BeautifulSoup = BeautifulSoup(sen.get(f"https://tixcraft.com{game_tag['data-href']}").content, features="html.parser")

print((time() - timer))
input("End..")
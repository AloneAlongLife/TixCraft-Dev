from bs4 import BeautifulSoup, Tag
from orjson import loads
from time import time
from numpy import frombuffer, uint8, full
from cv2 import imdecode, IMREAD_COLOR, cvtColor, COLOR_BGR2GRAY, INTER_NEAREST, resize
from webbrowser import get as w_get
from os.path import isfile, split
from os import get_terminal_size
from aiohttp import ClientSession
from aiofiles import open as a_open
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
from asyncio import create_task, gather, set_event_loop_policy, WindowsSelectorEventLoopPolicy, new_event_loop, sleep
from platform import system
from traceback import format_exception

async def print_vcode(_session: ClientSession):
    def longer(inp: list):
        return inp + [" " * 75] * (max_h - len(inp))
    async def read_img():
        _res = await _session.get("https://tixcraft.com/ticket/captcha")
        return await _res.content.read()
    wid = get_terminal_size().columns // 76

    print("取得驗證碼...")
    task = [
        create_task(
            read_img()
        ) for _ in range(3 * wid)
    ]
    _img_list = await gather(*task)

    out = []
    for i, _raw_img in enumerate(_img_list, 1):
        _img = imdecode(frombuffer(_raw_img, uint8), IMREAD_COLOR)
        _img = resize(cvtColor(_img, COLOR_BGR2GRAY), (75, 40), interpolation=INTER_NEAREST)

        temp = full(_img.shape, " ")
        temp[_img > 250] = "#"
        temp = [k for k in map("".join, temp.tolist()) if "#" in k]
        out.append(temp)

        if i % wid == 0:
            max_h = max(map(len, out))
            out = tuple(map(longer, out))
            _p = "\n".join(map("|".join, zip(*out)))
            print(_p)
            print("-" * get_terminal_size().columns)
            out = []

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition GX-CN)"
}
TIMEZONE = timezone(timedelta(hours=8))

async def main():
    url = f"https://tixcraft.com/activity/game/{split(input('URL :'))[1].strip()}"

    if isfile("SID.txt"):
        async with a_open("SID.txt", mode="r") as _file:
            sid = await _file.read()
        sid = sid.strip()
        print(f"自動讀取上次的SID: {sid}")
    else:
        sid = input("SID :").strip()
        async with a_open("SID.txt", mode="w") as _file:
            await _file.write(sid)

    try: ticket_num = int(input("Ticket Count :"))
    except: ticket_num = 1

    ticket_time = datetime.fromisoformat(input("售票時間 :"))

    session = ClientSession(
        headers=HEADERS,
        cookies={
            "SID": sid
        }
    )

    _res = await session.get(url)
    _game_page = BeautifulSoup(await _res.content.read(), features="html.parser")
    _game_title = _game_page.select_one('h2.activity-title').text

    __lest_time = ticket_time - datetime.now(TIMEZONE)
    while __lest_time > timedelta(seconds=5):
        await sleep(1)
        __lest_time = ticket_time - datetime.now(TIMEZONE)
        print(f"\"{_game_title}\"還剩餘 {__lest_time} 秒開賣", end="\r")
    print("\n開始抓取資料...")
    
    _seat_url = None
    while True:
        _res = await session.get(url)
        _game_page = BeautifulSoup(await _res.content.read(), features="html.parser")
        _input_list = _game_page.select("#gameList input")
        for _input in _input_list:
            if "text-center" not in _input.findNext().get("class"):
                _seat_url = urljoin("https://tixcraft.com/", _input["data-href"])
                break
        if _seat_url != None: break
        await sleep(0.3)
    
    timer = time()
    while True:
        _res = await session.get(_seat_url)
        _game_page = BeautifulSoup(await _res.content.read(), features="html.parser")

        _url_data: dict = loads(_game_page.decode().split("var areaUrlList = ")[1].split(";")[0].replace("\\", ""))
        _zone_list = _game_page.select("div.zone.area-list a")
        
        _game_id = _zone_list[min(2, len(_zone_list) - 1)]["id"]
        try:
            _order_url = urljoin("https://tixcraft.com/", _url_data[_game_id])
        except:
            _order_url = urljoin("https://tixcraft.com/", list(_url_data.values())[0])

        _res = await session.get(_order_url)
        _order_page = BeautifulSoup(await _res.content.read(), features="html.parser")

        await print_vcode(session)

        _form: Tag = _order_page.select_one("form")
        _agree = "TicketForm[agree]" + _order_page.decode().split('\"name\", \"TicketForm[agree]')[1].split('\");')[0]

        _form_data = {
            "CSRFTOKEN": _form.select_one("#CSRFTOKEN")["value"],
            _agree: 1,
            "ticketPriceSubmit": ""
        }
        _tick_list = _form.select("#ticketPriceList select")
        _tick_list_2 = _form.select("#ticketPriceList input")
        _form_data[_tick_list[0]["name"]] = ticket_num
        _form_data[_tick_list_2[0]["name"]] = _tick_list_2[0]["value"]
        for _tic, _pic in zip(_tick_list[1:], _tick_list_2[1:]):
            _form_data[_tic["name"]] = 0
            _form_data[_pic["name"]] = _pic["value"]

        while len(_vcode := input("請輸入驗證碼:")) != 4: print("驗證碼長度錯誤，請重新輸入!")
        _form_data["TicketForm[verifyCode]"] = _vcode

        try:
            await session.post(_order_url, data=_form_data)
            _res = await session.get("https://tixcraft.com/ticket/check")
            _content = await _res.content.read()
            _check_data = loads(_content)
        except Exception as e:
            print(f"已用時: {format(time() - timer, '.2f')} 秒")
            _mes = "".join(format_exception(e))
            print("搶票失敗...")
            print(_mes)
            async with a_open(f"{datetime.now(TIMEZONE).isoformat().replace(':', '_').replace('/', '-')}.error.log", mode="w") as _file:
                await _file.write(_mes)
            async with a_open(f"{datetime.now(TIMEZONE).isoformat().replace(':', '_').replace('/', '-')}.error.html", mode="wb") as _file:
                await _file.write(_content)
            print("重新開始搶票...")
            continue

        print(_check_data["message"])
        if _check_data["waiting"]:
            for i in range(_check_data["time"]):
                print(f"搶票成功 請等待{_check_data['time'] - i}秒...", end="\r")
                await sleep(1)
            print("搶票成功 請等待0秒... 請前往該帳號訂單查看: https://tixcraft.com/ticket/checkout")
            w_get("windows-default").open("https://tixcraft.com/ticket/checkout")
            break

    print(f"共計用時: {format(time() - timer, '.2f')} 秒")
    input("End..")

if __name__ == "__main__":
    if system() == "Windows": set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    try:
        loop = new_event_loop()
        loop.run_until_complete(main())
    except:
        pass
    loop.close()
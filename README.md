# TixCraft-Dev

## 注意事項

**凡使用機器人搶票皆有被鎖帳的風險~~畢竟手搶都會被鎖帳了~~，請評估後再進行使用，後果請自行承擔。**

## 使用方法

1.請先前往[Release](https://github.com/AloneAlongLife/TixCraft-Dev/releases)頁面下載最新版本的程式。
![Imgur](https://i.imgur.com/ayEo9TC.png)

2.下載完成後啟動程式，Windwos會跳出警示~~因為我沒買憑證~~，請按`其他資訊 > 仍要執行`

3.程式開啟後會依序顯示以下內容:
```
URL :
SID :
Ticket Count :
售票時間 :
```
填入說明:
 - URL
   - 要搶票的網址。
 - SID
    - 帳戶識別ID。
    - 取得方式:
       - 請於瀏覽器中登入`https://tixcraft.com/`。
       - 登入後在瀏覽器上方的網址列，最左邊(視瀏覽器而有不同)有個鎖頭，將它點開。
       - 點開依序點選`Cookie > tixcraft.com > Cookie > SID`並將值保存下來。
     - 上次使用的SID會保存於資料夾中的`SID.txt`
 - Ticket Count
    - 票數。
    - 請填入數字。
    - 若未輸入則會以`1`作為預設。
 - 售票時間
    - 發售時間，會到發售前5秒(本機時間)才開始發送請求，降低鎖帳風險。
    - ISO格式，需含時區，如發售時間為`2023/01/12 (四)12PM`，則應輸入的格式為`2023-01-12T12:00:00+08:00`。

4.隨後便會開始自動搶票，如果還沒開始發售，則會重複發送請求，直到開始發售。
![Imgur](https://i.imgur.com/0bBlbj0.png)

5.接著會跳出驗證碼，會有至少3張，驗證碼皆相同。

![Imgur](https://i.imgur.com/WDP7nQP.png)

6.搶票完成後會跳出訊息，並自動開啟瀏覽器前往[結帳頁面](https://tixcraft.com/checkout)，若在頁面中沒有出現訂單請等待4~8秒後再刷新頁面。

![Imgur](https://i.imgur.com/h7KhZ9D.png)

## 小叮嚀
1.請確保網路通暢，並且不要一次啟動太多支搶票程式，若在同時間內發送太多請求會被封鎖。

3.在搶票開始前請確保你的輸入法是英文輸入法，避免在驗證碼延宕太多時間，不管是哪一種機器人
幾乎無法通過圖形驗證，代表如果驗證碼打得越快，搶到票的機率就越高。

4.程式運行時建議使用全螢幕，這樣在看驗證碼比較方便。

5.請確保在[訂單頁面](https://tixcraft.com/order)沒有未完成的訂單，如果有請先取消或者進行付款，只要有選擇付款方式並送出即可，不一定要完成繳費。也可直接檢查[結帳頁面](https://tixcraft.com/ticket/checkout)。

合格範例 - 訂單頁面
![Imgur](https://i.imgur.com/ncwd62a.png)

合格範例 - 訂單頁面
![Imgur](https://i.imgur.com/W3hu1V3.png)

不合格範例 - 訂單頁面
![Imgur](https://i.imgur.com/y07FLLQ.png)

不合格範例 - 結帳頁面
![Imgur](https://i.imgur.com/UNVC5wl.png)

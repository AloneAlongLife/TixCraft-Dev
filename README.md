# TixCraft-Dev

## 使用方法

1.請先前往[Release](https://github.com/AloneAlongLife/TixCraft-Dev/releases)頁面下載最新版本的程式。
![Imgur](https://i.imgur.com/ayEo9TC.png)

2.下載完成後啟動程式，Windwos會跳出警示~~因為我沒買憑證~~，請按`其他資訊 > 仍要執行`

3.程式開啟後會依序顯示以下內容:
```
URL :
SID :
Ticket Count :
```
填入說明:
 - URL
   - 要搶票的場次列表的網址。
   - 格式為`https://tixcraft.com/activity/game/活動ID`，例如本次就是`https://tixcraft.com/activity/game/23_ssf4`。
   - 活動ID會在網址的最後，例如網址為`https://tixcraft.com/activity/detail/23_wbc`，那他的活動ID就是`23_wbc`，以此類推。
   - 如果頁面中有出現`立即購票`按鈕，可直接`右鍵 > 複製連結網址`
   - 可填入`test`測試是否能夠正常運作。
   - 若未輸入則會以`https://tixcraft.com/activity/game/23_ssf4`作為預設。
 - SID
    - 帳戶識別ID。
    - 取得方式:
       - 請於瀏覽器中登入`https://tixcraft.com/`。
       - 登入後在瀏覽器上方的網址列，最右邊(視瀏覽器而有不同)有個鎖頭，將它點開。
       - 點開依序點選`Cookie > tixcraft.com > Cookie > SID`並將值保存下來。
 - Ticket Count
    - 票數。
    - 請填入數字。
    - 若未輸入則會以`1`作為預設。

4.隨後便會開始自動搶票，如果還沒開始發售，則會重複發送請求，直到開始發售。
![Imgur](https://i.imgur.com/0bBlbj0.png)

5.接著會跳出驗證碼，一共9張，驗證碼皆相同。
:warning: 注意事項
```warning
1.當第一張驗證碼出現後即可開始輸入，不必等到9張皆出現，9張只是為了能夠方便辨識。
2.如果在輸出驗證碼的同時進行打字，在最後看到的字串不一定是完整的字串(例如輸入了`abcd`，最後看到的就只有`bcd`)，請不要擔心，那只是因為被驗證碼擠到上面去了，只要確定有輸入就可以安心送出，如果長度錯誤會有通知請你重新輸入。
```
![Imgur](https://i.imgur.com/WDP7nQP.png)
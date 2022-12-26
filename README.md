# Line Project
## Setup
### 需求
* Python 3.6
* Pipenv
* Ngrok
  * 下載網址: https://ngrok.com/download
### 前置作業
去LINE的官網註冊一個LINE bot\
然後將自己的 `.env` 中的 `LINE_CHANNEL_SECRET` 和 `LINE_CHANNEL_ACCESS_TOKEN` 替換成自己的\
開啟終端機執行
```sh
ngrok http 8000
```
得到網址之後將網址貼在Webhook URL的地方並在後方加上 `/webhook`\
再執行下方指令啟動LINE bot
```sh
pipenv run python app.py
```
## 架構
![fsm](https://github.com/stanlet2000/line_project/blob/main/fsm.png)
## How to play
開啟line bot後，隨便打字就可以觸發開始目錄，點擊目錄下方的開始即可進入遊戲\
![img](https://i.imgur.com/Mklgpwf.jpg)\
也可以直接打"start"進入遊戲\
![img](https://i.imgur.com/f2dKmTe.jpg)\
進入遊戲後只要點擊按鈕即可遊玩\
當需要輸入密碼時，直接在下方訊息傳送欄打出密碼並送出就可以解鎖\
![img](https://i.imgur.com/0tdtL0T.png)
## Walkthrough
### 這是防雷區
下方開始就是密室的攻略，不想被暴雷的可以直接跳過\
![rick](https://i.imgur.com/6KfIxHM.jpg)
---
1. 進入房間後向左轉，移動到房間左邊\
![img](https://i.imgur.com/L9sQDGC.jpg)
3. 點擊往前查看\
![img](https://i.imgur.com/YjdpWj9.jpg)
4. 先去察看地圖\
![img](https://i.imgur.com/32KWIjd.jpg)\
地圖的解法是將各房間的門都找到之後，就可以畫出一條路徑\
![img](https://i.imgur.com/poF65CI.jpg)
5. 解出藏寶圖之後便可以移動到旁邊的箱子\
輸入剛剛解出來的密碼即可打開箱子\
![img](https://i.imgur.com/g8wi8y6.jpg)\
密碼：右右下右下左左下右下右上右上右上左上右右
6. 打開箱子後便會看到一張海報\
![img](https://i.imgur.com/cZiaYPv.png)\
不同的顏色可以拼出不同數字
7. 離開箱子來到房間後面，後面有一扇門掛著四位密碼鎖\
用剛剛在海報上得到的數字對映鎖上的顏色，即可打開門\
![img](https://i.imgur.com/CleD8l6.jpg)
8. 進入小房間，點擊書架並查看書，會得到跟黑洞數有關的資訊\
![img](https://i.imgur.com/k1KbrPX.jpg)
9. 離開小房間，移動到房間右邊，去察看桌子會發現有個上鎖的抽屜\
![img](https://i.imgur.com/OZk1G5v.jpg)
10. 配合抽屜的提示可以知道跟黑洞數有關係\
利用剛剛得到的資訊找出黑洞數並輸入密碼\
![img](https://i.imgur.com/IEWUBKX.jpg)
11. 打開抽屜後，會得到一張密碼表\
![img](https://i.imgur.com/ZcRB8tO.png)
12. 回到小房間，查看保險箱\
會發現保險箱上有密碼表上的符號\
分別為 9、4、16\
![img](https://i.imgur.com/qDJOEaz.jpg)\
但此時這並不是正確的密碼\
我們需要再將它轉換成20進位
```math
9\times 20^2 + 4\times 20^1 + 16\times 20^0 = 3696
```
![img](https://i.imgur.com/z0HGlIW.jpg)\
12. 打開保險箱之後就會得到前門的鑰匙\
最後只要回到主房間把前門打開就破關了!!
![img](https://i.imgur.com/jA1WWru.jpg)

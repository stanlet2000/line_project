from transitions.extensions import GraphMachine
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction


from utils import send_text_message, send_button_message, send_image_and_button_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.back_door_unlock = False
        self.chest_unlock = False
        self.drawer_unlock = False
        self.front_door_unlock = False

    def get_start(self, event):
        text = event.message.text
        return text.lower() == "start"

    def is_going_to_main_room_front(self, event):
        text = event.message.text
        return text.lower() == "front"

    def is_going_to_front_door(self, event):
        text = event.message.text
        return text.lower() == "front door"

    def is_going_to_left(self, event):
        text = event.message.text
        return text.lower() == "left"

    def is_going_to_check_left(self, event):
        text = event.message.text
        return text.lower() == "check left"

    def is_going_to_map(self, event):
        text = event.message.text
        return text.lower() == "map"

    def is_going_to_chest(self, event):
        text = event.message.text
        return text.lower() == "chest"

    def is_going_to_poster(self, event):
        text = event.message.text
        if not self.chest_unlock:
            if text == "右右下右下左左下右下右上右上右上左上右右":
                self.chest_unlock = True
                return True
            
            
            send_button_message(
                event.reply_token,
                title = "密碼錯誤",
                text = "繼續輸入密碼還是離開?\n(小提示: 直接打字送出就能輸入密碼喔<3)",
                actions = [
                    {
                        "type": "message",
                        "label": "查看地圖",
                        "text": "map",
                    },
                    {
                        "type": "message",
                        "label": "返回",
                        "text": "check left",
                    },
                ],
            )
            return False
        
        return text.lower() == "poster"

    def is_going_to_right(self, event):
        text = event.message.text
        return text.lower() == "right"

    def is_going_to_table(self, event):
        text = event.message.text
        return text.lower() == "table"

    def is_going_to_drawer(self, event):
        text = event.message.text
        if self.drawer_unlock:
            return text.lower() == "drawer"
        
        if text == "6174":
            self.drawer_unlock = True
            return True
        
        send_button_message(
            event.reply_token,
            title = "密碼錯誤",
            text = "繼續輸入密碼還是離開?\n(小提示: 直接打字送出就能輸入密碼喔<3)",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "right",
                },
            ],
        )
        return False

    def is_going_to_back(self, event):
        text = event.message.text
        return text.lower() == "back"

    def is_going_to_back_door(self, event):
        text = event.message.text
        return text.lower() == "back door"

    def is_going_to_back_room(self, event):
        text = event.message.text
        if self.back_door_unlock:
            return text.lower() == "back room"
        
        print("door is locked\n")

        if text == "8693":
            self.back_door_unlock = True
            return True
        
        send_button_message(
            event.reply_token,
            title = "密碼錯誤",
            text = "繼續輸入密碼還是離開?\n(小提示: 直接打字送出就能輸入密碼喔<3)",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "back",
                },
            ],
        )
        return False
        
        

    def leave_back_room(self, event):
        text = event.message.text
        return text.lower() == "go back"

    def hanging_in_back_room(self, event):
        text = event.message.text
        return text.lower() == "back room"

    def is_going_to_bookshelf(self, event):
        text = event.message.text
        return text.lower() == "bookshelf"

    def is_going_to_book(self, event):
        text = event.message.text
        return text.lower() == "book"

    def is_going_to_safe(self, event):
        text = event.message.text
        return text.lower() == "safe"


    def is_going_to_get_key(self, event):
        text = event.message.text

        if not text == "3696":
            send_button_message(
                event.reply_token,
                title = "密碼錯誤",
                text = "繼續輸入密碼還是離開?\n(小提示: 好像要換成20進位喔<3)",
                actions = [
                    {
                        "type": "message",
                        "label": "返回",
                        "text": "back room",
                    },
                ],
            )
            return False
        
        return True

    def is_going_to_Congratulation(self, event):
        text = event.message.text
        if not text.lower() == "go out":
            return False
        
        if self.front_door_unlock:
            return True

        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "前門",
            text = "門上鎖了\n需要鑰匙才能打開",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "front",
                },
            ],
        )
        return False

    def restart(self, event):
        text = event.message.text
        
        return text.lower() == "restart"
            


    def on_enter_start(self, event):
        print("start!!")

        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "開始目錄",
            text = "歡迎，點擊下方的【開始】來進行遊戲",
            actions = [
                {
                    "type": "message",
                    "label": "開始",
                    "text": "start"
                },
            ]
        )
    
    def on_enter_main_room_front(self, event):
        print("front\n")

        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "主房間正面",
            text = "主房間的正面有一扇門，要過去看看嗎?",
            actions = [
                {
                    "type": "message",
                    "label": "開門",
                    "text": "front door"
                },
                {
                    "type": "message",
                    "label": "往左走",
                    "text": "left"
                },
                {
                    "type": "message",
                    "label": "往右走",
                    "text": "right"
                },
                {
                    "type": "message",
                    "label": "向後轉",
                    "text": "back"
                },
            ]
        )

    
    def on_enter_front_door(self, event):
        print("front door\n")


        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "前門",
            text = "好像被鎖起來了，要打開嗎?",
            actions = [
                {
                    "type": "message",
                    "label": "打開",
                    "text": "go out"
                },
                {
                    "type": "message",
                    "label": "返回",
                    "text": "front"
                },
            ]
        )

    def on_enter_left(self, event):
        print("left\n")
        

        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "主房間左邊",
            text = "主房間左邊的牆角放著一個箱子，牆上貼著一張地圖，要過去看看嗎?",
            actions = [
                {
                    "type": "message",
                    "label": "往前看看",
                    "text": "check left",
                },
                {
                    "type": "message",
                    "label": "往左走",
                    "text": "back",
                },
                {
                    "type": "message",
                    "label": "往右走",
                    "text": "front",
                },
                {
                    "type": "message",
                    "label": "向後轉",
                    "text": "right",
                },
            ],
        )

    def on_enter_check_left(self, event):
        print("check left\n")
        

        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "主房間左邊",
            text = "要先查看哪個?",
            actions = [
                {
                    "type": "message",
                    "label": "查看地圖",
                    "text": "map",
                },
                {
                    "type": "message",
                    "label": "查看箱子",
                    "text": "chest",
                },
                {
                    "type": "message",
                    "label": "返回",
                    "text": "left",
                },
            ],
        )

    def on_enter_map(self, event):
        print("show map\n")
        
        reply_token = event.reply_token
        send_image_and_button_message(
            reply_token,
            title = "藏寶圖",
            text = "一張奇怪的藏寶圖，好像有謎題可以解",
            actions = [
                {
                    "type": "message",
                    "label": "查看箱子",
                    "text": "chest",
                },
                {
                    "type": "message",
                    "label": "返回",
                    "text": "check left",
                },
            ],
            url = "https://i.imgur.com/poF65CI.jpg",
        )

    def on_enter_chest(self, event):
        print("chest\n")
        
        reply_token = event.reply_token
        if self.chest_unlock:
            send_button_message(
                reply_token,
                title = "箱子",
                text = "毫無反應，就是普通的箱子",
                actions = [
                    {
                        "type": "message",
                        "label": "查看地圖",
                        "text": "map",
                    },
                    {
                        "type": "message",
                        "label": "查看海報",
                        "text": "poster",
                    },
                    {
                        "type": "message",
                        "label": "返回",
                        "text": "check left",
                    },
                ],
            )
        else:
            send_button_message(
                reply_token,
                title = "上鎖的箱子",
                text = "箱子掛個一個方向鎖，要輸入密碼還是離開?\n(小提示: 直接打字送出就能輸入密碼喔<3)",
                actions = [
                    {
                        "type": "message",
                        "label": "查看地圖",
                        "text": "map",
                    },
                    {
                        "type": "message",
                        "label": "返回",
                        "text": "check left",
                    },
                ],
            )

    def on_enter_poster(self, event):
        print("show poster\n")
        
        reply_token = event.reply_token
        send_image_and_button_message(
            reply_token,
            title = "數字海報",
            text = "一張寫著數字的海報，每個數字都有不同顏色",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "left",
                },
            ],
            url = "https://i.imgur.com/cZiaYPv.png"
        )


    def on_enter_right(self, event):
        print("right\n")
        
        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "主房間右邊",
            text = "房間的右邊有張桌子",
            actions = [
                {
                    "type": "message",
                    "label": "查看桌子",
                    "text": "table",
                },
                {
                    "type": "message",
                    "label": "往左走",
                    "text": "front",
                },
                {
                    "type": "message",
                    "label": "往右走",
                    "text": "back",
                },
                {
                    "type": "message",
                    "label": "向後轉",
                    "text": "left",
                },
            ],
        )

    def on_enter_table(self, event):
        print("table\n")
        reply_token = event.reply_token

        if self.drawer_unlock:
            send_button_message(
                reply_token,
                title = "桌子",
                text = "要開抽屜嗎?",
                actions = [
                    {
                        "type": "message",
                        "label": "抽屜",
                        "text": "drawer",
                    },
                    {
                        "type": "message",
                        "label": "返回",
                        "text": "right",
                    },
                ],
            )
        
        else:
            send_button_message(
                reply_token,
                title = "桌子",
                text = "桌子下有個被鎖著的抽屜，抽屜上有個奇怪的花紋，看起來像黑洞?\n(輸入四位密碼以嘗試解鎖)",
                actions = [
                    {
                        "type": "message",
                        "label": "返回",
                        "text": "right",
                    },
                ],
            )
        

    def on_enter_drawer(self, event):
        print("show pic in drawer\n")
        
        reply_token = event.reply_token
        send_image_and_button_message(
            reply_token,
            title = "抽屜",
            text = "這是什麼?",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "right",
                },
            ],
            url ="https://i.imgur.com/ZcRB8tO.png",
        )

    def on_enter_back(self, event):
        print("back\n")
        
        reply_token = event.reply_token
        if self.back_door_unlock:
            send_button_message(
                reply_token,
                title = "主房間後面",
                text = "主房間後面",
                actions = [
                    {
                        "type": "message",
                        "label": "進小房間",
                        "text": "back room"
                    },
                    {
                        "type": "message",
                        "label": "往左走",
                        "text": "right"
                    },
                    {
                        "type": "message",
                        "label": "往右走",
                        "text": "left"
                    },
                    {
                        "type": "message",
                        "label": "向後轉",
                        "text": "front"
                    },
                ]
            )
        
        else:
            send_button_message(
                reply_token,
                title = "主房間後面",
                text = "主房間後面有一扇門，似乎通往其他房間",
                actions = [
                    {
                        "type": "message",
                        "label": "開門",
                        "text": "back door"
                    },
                    {
                        "type": "message",
                        "label": "往左走",
                        "text": "right"
                    },
                    {
                        "type": "message",
                        "label": "往右走",
                        "text": "left"
                    },
                    {
                        "type": "message",
                        "label": "向後轉",
                        "text": "front"
                    },
                ]
            )

    def on_enter_back_door(self, event):
        print("back door\n")
        
        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "主房間後面",
            text = "門被上鎖了，鎖頭上有四個顏色，順序是【棕、黃、白、橘】",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "back"
                },
            ]
        )


    def on_enter_back_room(self, event):
        print("back room\n")
        
        reply_token = event.reply_token
        if not self.front_door_unlock:
            send_button_message(
                reply_token,
                title = "小房間",
                text = "你進到小房間，房間裡除了書架和一個保險箱之外，其他什麼都沒有",
                actions = [
                    {
                        "type": "message",
                        "label": "查看書櫃",
                        "text": "bookshelf"
                    },
                    {
                        "type": "message",
                        "label": "查看保險箱",
                        "text": "safe"
                    },
                    {
                        "type": "message",
                        "label": "返回主房間",
                        "text": "go back"
                    },
                ]
            )
        else:
            send_button_message(
                reply_token,
                title = "小房間",
                text = "拿到鑰匙，可以離開了!!",
                actions = [
                    {
                        "type": "message",
                        "label": "返回主房間",
                        "text": "go back"
                    },
                ]
            )

    def on_enter_bookshelf(self, event):
        print("bookshelf\n")
        
        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "書架",
            text = "架上有一本書有夾書籤，要拿起來看嗎?",
            actions = [
                {
                    "type": "message",
                    "label": "翻書",
                    "text": "book"
                },
                {
                    "type": "message",
                    "label": "查看保險箱",
                    "text": "safe"
                },
                {
                    "type": "message",
                    "label": "返回",
                    "text": "back room"
                },
            ]
        )

    def on_enter_book(self, event):
        print("show book\n")
        
        reply_token = event.reply_token
        send_image_and_button_message(
            reply_token,
            title = "書",
            text = "夾書籤的那一頁在介紹一個叫【黑洞數】的東西",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "bookshelf"
                },
            ],
            url = "https://i.imgur.com/b7UBuPr.png",
        )

    def on_enter_safe(self, event):
        print("safe\n")
        
        reply_token = event.reply_token
        send_image_and_button_message(
            reply_token,
            title = "保險箱",
            text = "一個上面有奇怪符號的保險箱，要解鎖看看嗎?\n(輸入四位密碼以解鎖)",
            actions = [
                {
                    "type": "message",
                    "label": "查看書架",
                    "text": "bookshelf"
                },
                {
                    "type": "message",
                    "label": "返回",
                    "text": "back room"
                },
            ],
            url = "https://i.imgur.com/ukJPGWz.jpg",
        )



    def on_enter_get_key(self, event):
        print("get key\n")
        self.front_door_unlock = True

        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "打開保險箱",
            text = "裡面有一把鑰匙",
            actions = [
                {
                    "type": "message",
                    "label": "返回",
                    "text": "back room"
                },
            ],
        )

    def on_enter_Congratulation(self, event):
        print("Congratulation\n")
        self.back_door_unlock = False
        self.chest_unlock = False
        self.drawer_unlock = False
        self.front_door_unlock = False

        reply_token = event.reply_token
        send_button_message(
            reply_token,
            title = "恭喜通關",
            text = "按下【重新開始】可以再次遊玩",
            actions = [
                {
                    "type": "message",
                    "label": "重新開始",
                    "text": "restart"
                },
            ],
        )


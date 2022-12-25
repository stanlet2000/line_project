import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_and_button_message

load_dotenv()


machine = TocMachine(
    states=["start", "main_room_front", "front_door", "left", "check_left", "poster", "chest", "map", "right", "table", "drawer", "back", "back_door", "back_room", "bookshelf", "book", "safe", "get_key", "Congratulation"],
    transitions=[
        {
            "trigger": "advance",
            "source": "start",
            "dest": "main_room_front",
            "conditions": "get_start",
        },
        {
            "trigger": "advance",
            "source": ["front_door", "main_room_front", "left", "right", "back",],
            "dest": "main_room_front",
            "conditions": "is_going_to_main_room_front",
        },
        {
            "trigger": "advance",
            "source": ["front_door", "main_room_front",],
            "dest": "front_door",
            "conditions": "is_going_to_front_door",
        },
        {
            "trigger": "advance",
            "source": ["poster", "check_left", "main_room_front", "left", "right", "back"],
            "dest": "left",
            "conditions": "is_going_to_left",
        },
        {
            "trigger": "advance",
            "source": ["left", "map", "chest",],
            "dest": "check_left",
            "conditions": "is_going_to_check_left",
        },
        {
            "trigger": "advance",
            "source": ["map", "chest", "check_left",],
            "dest": "map",
            "conditions": "is_going_to_map",
        },
        {
            "trigger": "advance",
            "source": ["map", "chest", "check_left",],
            "dest": "chest",
            "conditions": "is_going_to_chest",
        },
        {
            "trigger": "advance",
            "source": "chest",
            "dest": "poster",
            "conditions": "is_going_to_poster",
        },
        {
            "trigger": "advance",
            "source": ["table", "drawer", "main_room_front", "left", "right", "back"],
            "dest": "right",
            "conditions": "is_going_to_right",
        },
        {
            "trigger": "advance",
            "source": ["table", "right",],
            "dest": "table",
            "conditions": "is_going_to_table",
        },
        {
            "trigger": "advance",
            "source": "table",
            "dest": "drawer",
            "conditions": "is_going_to_drawer",
        },
        {
            "trigger": "advance",
            "source": ["back_door", "main_room_front", "left", "right", "back",],
            "dest": "back",
            "conditions": "is_going_to_back",
        },
        {
            "trigger": "advance",
            "source": ["back_door", "back",],
            "dest": "back_door",
            "conditions": "is_going_to_back_door",
        },
        {
            "trigger": "advance",
            "source": ["back_door", "back",],
            "dest": "back_room",
            "conditions": "is_going_to_back_room",
        },
        {
            "trigger": "advance",
            "source": "back_room",
            "dest": "main_room_front",
            "conditions": "leave_back_room",
        },
        {
            "trigger": "advance",
            "source": ["back_room", "bookshelf", "safe", "get_key",],
            "dest": "back_room",
            "conditions": "hanging_in_back_room",
        },
        {
            "trigger": "advance",
            "source": ["back_room", "bookshelf", "safe", "book",],
            "dest": "bookshelf",
            "conditions": "is_going_to_bookshelf",
        },
        {
            "trigger": "advance",
            "source": "bookshelf",
            "dest": "book",
            "conditions": "is_going_to_book",
        },
        {
            "trigger": "advance",
            "source": ["back_room", "bookshelf", "safe",],
            "dest": "safe",
            "conditions": "is_going_to_safe",
        },
        {
            "trigger": "advance",
            "source":  "safe",
            "dest": "get_key",
            "conditions": "is_going_to_get_key",
        },
        {
            "trigger": "advance",
            "source":  "front_door",
            "dest": "Congratulation",
            "conditions": "is_going_to_Congratulation",
        },
        {
            "trigger": "advance",
            "source":  "Congratulation",
            "dest": "start",
            "conditions": "restart",
        },
        # {"trigger": "unlock_back_door", "source": ["back_door", "back",], "dest": "unlock_back_door"},
    ],
    initial="start",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


# @app.route("/callback", methods=["POST"])
# def callback():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue

#         # send_text_message(event.reply_token, "救命啊啊啊")
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.message.text)
#         )

#     return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        # print("in la!!\n")

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if machine.state == "start":
                reply_token = event.reply_token
                
                # messages = [
                #     "123","234"
                # ]
                # send_text_message(reply_token, messages)

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
                    ],
                )
            try:
                send_text_message(event.reply_token, ["操作錯誤"])
            except:
                pass



    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port)
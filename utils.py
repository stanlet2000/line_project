import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, ImageSendMessage



channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, texts):
    line_bot_api = LineBotApi(channel_access_token)
    messages = []
    for text in texts:
        messages.append(TextSendMessage(text))
    line_bot_api.reply_message(reply_token, messages)

    return "OK"

def send_button_message(reply_token, **template):
    line_bot_api = LineBotApi(channel_access_token)
    button = TemplateSendMessage(
        alt_text = 'button',
        template = ButtonsTemplate(
            title = template["title"],
            text = template["text"],
            actions = template["actions"],
        ),
    )
    try:
        button.template.thumbnailImageUrl = template["url"]
    except:
        pass

    line_bot_api.reply_message(reply_token, button)

    return "OK"

def send_image_and_button_message(reply_token, **template):
    line_bot_api = LineBotApi(channel_access_token)
    button = TemplateSendMessage(
        alt_text = 'button',
        template = ButtonsTemplate(
            title = template["title"],
            text = template["text"],
            actions = template["actions"],
        ),
    )

    image = ImageSendMessage(
        original_content_url = template["url"],
        preview_image_url = template["url"],
    )
    
    messages = [image, button]
    line_bot_api.reply_message(reply_token, messages)

    return "OK"


"""
def send_image_url(id, img_url):
    pass
"""

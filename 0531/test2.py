from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

channel_access_token = '8SiBzc1GFPHK/lcN5mhM2htKcp656kyFWbF5gO8+YqrEd7o1tWcKZH8H+itRorSk1d1/q7yyUkdVyMlVrAh3Ok+6m2z9EzM3hduaxyAIPO+DWebiXEobIivxTU4kPcfnWoXaaryIC1vGFJZfaTdm9QdB04t89/1O/w1cDnyilFU='
channel_secret = 'd50ccd681598032c47bd875ae83b04bb'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
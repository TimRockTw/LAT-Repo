import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import requests

app = Flask(__name__)

# Line Bot的Channel Access Token和Channel Secret
channel_access_token = '8SiBzc1GFPHK/lcN5mhM2htKcp656kyFWbF5gO8+YqrEd7o1tWcKZH8H+itRorSk1d1/q7yyUkdVyMlVrAh3Ok+6m2z9EzM3hduaxyAIPO+DWebiXEobIivxTU4kPcfnWoXaaryIC1vGFJZfaTdm9QdB04t89/1O/w1cDnyilFU='
channel_secret = 'd50ccd681598032c47bd875ae83b04bb'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# Azure Text Analytics
endpoint = 'https://bx9aaf.cognitiveservices.azure.com/'
api_key = '41005bbb75eb4d2b9dc81fa6f083e4ef'
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

@app.route("/callback", methods=['POST'])
def callback():
    # 接收Line Server傳送的訊息
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    # 處理訊息事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 接收使用者傳送的訊息
    text = event.message.text

    # 執行情感分析
    response = text_analytics_client.analyze_sentiment([text], language="zh-Hant", include_opinion_mining=True)
    sentiment = response[0].sentiment
    confidence_score = response[0].confidence_scores[sentiment]

    opinion_text = ""
    if response[0].sentences[0].opinions:
        opinion_text = response[0].sentences[0].opinions[0].target.text

    # 儲存至JSON Server
    data = {
        "sentiment": sentiment,
        "confidenceScore": confidence_score,
        "opinionText": opinion_text
    }
    url = "https://bx9aaf.azurewebsites.net/reviews"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)

    reply_text = f"\n情感：{sentiment}\n信心指數：{confidence_score:.2f}"
    if opinion_text:
        reply_text += f"\n主詞：{opinion_text}"

    # 回覆使用者訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()

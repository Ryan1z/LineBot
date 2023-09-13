from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot import LineBotApi
from linebot.models import ImageMessage, ImageSendMessage
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
from ai import chat,image
import os

app = Flask(__name__)

CHANNEL_SECRET="" #token
CHANNEL_ACCESS_TOKEN=""#token

@app.route("/", methods=['GET'])
def home():
    return "Hi"

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)

    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        
        image_url = image(msg)
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        
        line_bot_api.reply_message(tk, image_message)     # 回傳圖片
    
    except Exception as e:
        print('error: ' + str(e))
    return 'OK'

app.run(port="5000")
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot import LineBotApi
from linebot.models import ImageMessage, ImageSendMessage
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
import datetime
from ai import chat,image

app = Flask(__name__)

CHANNEL_SECRET = ""      #TOKEN
CHANNEL_ACCESS_TOKEN = ""#TOKEN

@app.route("/", methods=['GET'])
def home():
    return "Connection Successful"

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    Data = json_data['events'][0]
    
    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = Data['replyToken']
        msg = Data['message']['text']
        text_message = TextSendMessage(text = chat(msg))
        line_bot_api.reply_message(tk, text_message)
        
        # 傳送者資訊
        userID = Data['source']['userId']
        userProfile = line_bot_api.get_profile(userID)
        userName = userProfile.display_name       
        userPicture = userProfile.picture_url     

        # 時間戳記
        Time = Data['timestamp']
        utcTime = datetime.datetime.utcfromtimestamp(Time / 1000.0)
        timeFormat = "%Y-%m-%d %H:%M:%S"
        localTime = utcTime + datetime.timedelta(hours=8)
        sendTime = localTime.strftime(timeFormat)
        
        #訊息型態
        messageType = Data['message']['type']
        
        userRequest = {"Time":sendTime,"MessageType":messageType,"UserInput":msg,"UserName":userName,"UserPicture":userPicture}
        print(userRequest)
        
        with open("text.json","a",encoding="utf-8") as fp:
            json.dump(userRequest,fp,ensure_ascii=False,indent=4)
            fp.write("\n")
                  
    except:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = Data['replyToken']
        messageType = Data['message']['type']
        
        userID = Data['source']['userId']
        userProfile = line_bot_api.get_profile(userID)
        userName = userProfile.display_name       
        userPicture = userProfile.picture_url     

        Time = Data['timestamp']
        utcTime = datetime.datetime.utcfromtimestamp(Time / 1000.0)
        timeFormat = "%Y-%m-%d %H:%M:%S"
        localTime = utcTime + datetime.timedelta(hours=8)
        sendTime = localTime.strftime(timeFormat)
               
        if messageType in ['image', 'audio', 'sticker', 'video', 'location', 'action']:
            errorRequest = '寫一則20字內回應關於目前不支援此類型的訊息 請改用文字詢問'
            text_message = TextSendMessage(text = chat(errorRequest))
            line_bot_api.reply_message(tk, text_message)
        
        userRequest = {"Time":sendTime,"MessageType":messageType,"UserInput":"Error Message Type: "+ messageType,"UserName":userName,"UserPicture":userPicture}
        print(userRequest)
        
        with open("error.json","a",encoding="utf-8") as fp:
            json.dump(userRequest,fp,ensure_ascii=False,indent=4)
            fp.write("\n")
                  
    return 'OK'

app.run(port="5000")
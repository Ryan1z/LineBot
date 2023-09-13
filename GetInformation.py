from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import ImageSendMessage, TextSendMessage
import json
from ai import chat, image  # 請確保 ai 模組中有 chat 和 image 函數
import os
import platform
import subprocess

app = Flask(__name__)

CHANNEL_SECRET = "" #TOKEN
CHANNEL_ACCESS_TOKEN = ""#TOKEN

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

        # 檢查用戶訊息，如果是特定指令，則執行相應的操作
        if msg == "查詢裝置資訊":
            device_info = get_device_info()
            reply_message = "您的裝置資訊：\n" + device_info
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_message))
        else:
            # 其他訊息的回覆
            reply_message = "感謝您的訊息！"
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_message))
    
    except Exception as e:
        print('error: ' + str(e))
    return 'OK'

def get_device_info():
    system_info = platform.system()
    machine_info = platform.machine()
    version_info = platform.version()
    processor_info = platform.processor()
    
    # 獲取記憶體和硬碟使用情況
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    
    device_info = f"作業系統：{system_info}\n裝置型號：{machine_info}\n作業系統版本：{version_info}\n處理器：{processor_info}\n"
    device_info += f"記憶體和硬碟使用情況：\n{memory_info}\n{disk_info}"
    
    return device_info

def get_memory_info():
    try:
        if platform.system() == 'Windows':
            # 使用chcp命令將命令提示符編碼設置為UTF-8
            subprocess.run("chcp 65001", shell=True)
            # 使用UTF-8編碼執行systeminfo命令
            result = subprocess.check_output(["systeminfo"], encoding='utf-8')
        else:
            result = subprocess.check_output(["free", "-h"]).decode("utf-8")
        return result
    except Exception as e:
        return str(e)
    
def get_disk_info():
    try:
        if platform.system() == 'Windows':
            result = subprocess.check_output(["wmic", "logicaldisk", "get", "size,freespace,caption"]).decode("cp437")
            # 解析硬碟資訊
            lines = result.strip().split('\n')
            headers = lines[0].split()
            data = lines[1].split()
            caption_index = headers.index('Caption')
            free_space_index = headers.index('FreeSpace')
            size_index = headers.index('Size')
            
            # 取得C槽的剩餘空間和已使用空間（以GB為單位）
            c_drive = next((line for line in lines[1:] if 'C:' in line), None)
            if c_drive:
                c_drive_data = c_drive.split()
                free_space = int(c_drive_data[free_space_index]) // (1024 ** 3)  # 轉換為GB
                size = int(c_drive_data[size_index]) // (1024 ** 3)  # 轉換為GB
                used_space = size - free_space
            else:
                free_space = "N/A"
                used_space = "N/A"
                
            d_drive = next((line for line in lines[1:] if 'D:' in line), None)
            if d_drive:
                d_drive_data = d_drive.split()
                D_free_space = int(d_drive_data[free_space_index]) // (1024 ** 3)  # 轉換為GB
                size = int(d_drive_data[size_index]) // (1024 ** 3)  # 轉換為GB
                D_used_space = size - D_free_space
            else:
                free_space = "N/A"
                used_space = "N/A"
            
            notebookInfo = f"C槽剩餘空間：{free_space}GB，已使用空間：{used_space}GB" + "\n" + f"D槽剩餘空間：{D_free_space}GB，已使用空間：{D_used_space}GB"
            
            return notebookInfo
        else:
            result = subprocess.check_output(["df", "-h"]).decode("utf-8")
            return result
    except Exception as e:
        return str(e)
    
if __name__ == "__main__":
    app.run(port="5000")

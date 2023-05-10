from PIL import Image
import openai
import os
from io import BytesIO
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat(msg):
      openai.api_key = os.getenv("OPENAI_API_KEY")
      msg = msg
      res = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[{"role":"user","content":msg}])
      res1 = res["choices"][0]["message"]["content"].replace("\n","")
      return res1


def image(msg):
    response = openai.Image.create(
        prompt=msg,
        size="256x256",
        n=1
    )
    imageUrl = response['data'][0]['url']
    
    return imageUrl

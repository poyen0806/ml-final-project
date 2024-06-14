import google.generativeai as genai
from configparser import ConfigParser
import os
# Config Parser
config = ConfigParser()
config.read("config.ini")
genai.configure(api_key=config["Gemini"]["API_KEY"])
os.environ["google_api_key"] = config["Gemini"]["API_KEY"]

from langchain_google_genai import ChatGoogleGenerativeAI

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
response = chat.send_message("你現在是一個健身教練，只能夠回答關於健身的問題，若問題跟健身無關請回答:我無法回答。除非有問飲食建議，否則不用給予")
response = chat.send_message("我想要訓練我的三頭肌，有什麼更好的建議。")
response = chat.send_message("要怎麼追求女生")

print(response.text)
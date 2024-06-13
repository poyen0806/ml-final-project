import google.generativeai as genai
from configparser import ConfigParser
import os
# Config Parser
config = ConfigParser()
config.read("config.ini")
genai.configure(api_key=config["Gemini"]["API_KEY"])
os.environ["google_api_key"] = config["Gemini"]["API_KEY"]

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
user_input = "性別:女、年齡:20、體重:60、身高:170、體脂率:20、左手肌肉:3、右手肌肉:2.9、軀幹:17、左腳肌肉:6、右腳肌肉:6.5"

model = ChatGoogleGenerativeAI(model = "gemini-pro")
Ques = "請根據給予的inbody數據分析以下項目:需要增肌或減脂?、上肢是否左右不平衡?、下肢是否左右不平衡?、上下肢是否不平衡?，這些資訊請用table儲存，不須其他文字說明。資料:"+user_input
result = model.invoke(Ques)
print(result.content)

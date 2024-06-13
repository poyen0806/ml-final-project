from langchain_google_genai import ChatGoogleGenerativeAI
from configparser import ConfigParser
import os

# Config Parser
config = ConfigParser()
config.read("config.ini")
os.environ["GOOGLE_API_KEY"] = config["Gemini"]["API_KEY"]

# Importing the ChatGoogleGenerativeAI class
L1_llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=False)
L2_llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=False)
L3_llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=False)

# Get user inbody data
import random
inbody = {
    "Gender": random.choice(["Male", "Female"]), # 性別
    "Age": random.randint(18, 65), # 年齡
    "Height": round(random.uniform(150, 190), 1), # 身高
    "Weight": round(random.uniform(50, 100), 1), # 體重
    "Skeletal Muscle Weight": round(random.uniform(20, 50), 1), # 骨骼肌重
    "Body Fat Weight": round(random.uniform(5, 20), 1), # 脂肪重
    "Body Fat Index": round(random.uniform(10, 40), 1), # 脂肪指數
    "Body Fat Percentage": round(random.uniform(10, 40), 1), # 脂肪百分比
    "Basal Metabolic Rate": round(random.uniform(1000, 2000), 1), # 基礎代謝率
    "Body Water": round(random.uniform(50, 70), 1), # 體水分
    "Left Hand Muscle Mass": round(random.uniform(1, 4), 2), # 左手肌肉量
    "Right Hand Muscle Mass": round(random.uniform(1, 4), 2), # 右手肌肉量
    "Left Leg Muscle Mass": round(random.uniform(5, 12), 2), # 左腿肌肉量
    "Right Leg Muscle Mass": round(random.uniform(5, 12), 2), # 右腿肌肉量
    "Trunk Muscle Mass": round(random.uniform(20, 50), 2), # 軀幹肌肉量
}

# Convert inbody data to a human-readable string
inbody_message = "\n".join([f"{key}: {value}" for key, value in inbody.items()])

# Use inbody message to generate analysis (LLM1)
from langchain_core.messages import SystemMessage, HumanMessage

L1_result = L1_llm.invoke(
    [
        SystemMessage(content="根據以下資訊，分析要減脂還是增肌？上肢左右是否不平衡？下肢左右是否不平衡？整體身體是否平衡？"),
        HumanMessage(content=inbody_message)
    ]
)
print(L1_result.content)

# Use L1_result to generate a menu (LLM2)
L2_result = L2_llm.invoke(
    [
        SystemMessage(content="根據您的健康檢查報告，為您生成一週的健身菜單。以下是您的健身建議和計劃："),
        HumanMessage(content=L1_result.content)
    ]
)
print(L2_result.content)

# Translate the menu into traditional Chinese (LLM3)
L3_result = L3_llm.invoke(
    [
        SystemMessage(content="將健身菜單翻譯成繁體中文。"),
        HumanMessage(content=L2_result.content)
    ]
)
print(L3_result.content)

# 他三層都生不出我要的東西
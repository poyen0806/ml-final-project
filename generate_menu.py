import google.generativeai as genai
from configparser import ConfigParser

# Config Parser
config = ConfigParser()
config.read("config.ini")
genai.configure(api_key=config["Gemini"]["API_KEY"])

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

# Initialize the generative model and give some simple advice
llm = genai.GenerativeModel('gemini-1.5-flash')
chat = llm.start_chat(history=[])
result = chat.send_message("你是一個健身教練，只能夠回答關於健身的問題，若問題跟健身無關請回答:我無法回答。不提供飲食建議。")
result = chat.send_message("現在有一個身體數據，請問你能幫忙分析嗎？要減脂還是增肌？上下肢哪裡需要加強？需要增強哪些肌肉？")
result = chat.send_message(inbody_message)
print(result.text)

# Generate a workout menu based on the advice
result = chat.send_message("請幫忙設計一個適合的訓練菜單，動作名稱、組數、每組做多少次請詳細說明。只需提供訓練菜單，不用提供飲食建議。")
print(result.text)
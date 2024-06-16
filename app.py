# import modules
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import matplotlib.image as mpimg
import keras.utils as image_utils
from keras.applications.vgg16 import preprocess_input
import time
from flask_markdown import markdown
from flask import Flask, render_template, flash, redirect, url_for, request
from form import TrainingForm, PhotoForm
from configparser import ConfigParser
import google.generativeai as genai
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'mysecretkey'
markdown(app)
config = ConfigParser()
config.read("config.ini")
genai.configure(api_key=config["Gemini"]["API_KEY"])

@app.route('/css')
def index():
    return render_template('css.html')
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/photo', methods=['POST', 'GET'])
def photo():
    form = PhotoForm()
    photo = None

    if form.validate_on_submit():
        photo = form.photo.data
        photo.save(os.path.join('static', 'tmp.jpg'))
        flash('Files uploaded successfully', 'success')
        Posture()
        return render_template('photo.html',form = form,photo='Show.jpg')  # Redirect to the same page after successful submission
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}")
        return render_template('photo.html',form=form)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    form = TrainingForm()
    data = None
    workout_menu = None
    
    if form.validate_on_submit():
        data = {
            'Gender': form.Gender.data,
            'Age': form.Age.data,
            'Height': form.Height.data,
            'Weight': form.Weight.data,
            'SkeletalMuscleWeight': form.SkeletalMuscleWeight.data,
            'BodyFatWeight': form.BodyFatWeight.data,
            'BodyFatIndex': form.BodyFatIndex.data,
            'BodyFatPercentage': form.BodyFatPercentage.data,
            'BasalMetabolicRate': form.BasalMetabolicRate.data,
            'BodyWater': form.BodyWater.data,
            'LeftHandMuscleMass': form.LeftHandMuscleMass.data,
            'RightHandMuscleMass': form.RightHandMuscleMass.data,
            'LeftLegMuscleMass': form.LeftLegMuscleMass.data,
            'RightLegMuscleMass': form.RightLegMuscleMass.data,
            'TrunkMuscleMass': form.TrunkMuscleMass.data
        }
        workout_menu = generate_workout_menu(data)
        flash('Workout Menu Generated Successfully', 'success')
        return render_template('output.html', workout_menu=workout_menu)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}")
    return render_template('menu.html', form=form, data=data, workout_menu=workout_menu)
@app.route('/output', methods=['GET', 'POST'])
def output():
    return render_template('output.html')
def generate_workout_menu(data):
    # Initialize the generative model and give some simple advice
    llm = genai.GenerativeModel('gemini-1.5-flash')
    chat = llm.start_chat(history=[])
    result = chat.send_message("你是一個健身教練，只能夠回答關於健身的問題。不提供飲食建議。禁止使用簡體中文，有礙觀瞻。")
    result = chat.send_message("現在有一個身體數據，請問你能幫忙分析嗎？要減脂還是增肌？上下肢哪裡需要加強？需要增強哪些肌肉？若左右有不平衡請說明要增強哪裡?")
    
    # Convert data to a format suitable for send_message
    data_str = f"性別: {data['Gender']}, 年齡: {data['Age']}, 身高: {data['Height']}, 體重: {data['Weight']}, 骨骼肌重量: {data['SkeletalMuscleWeight']}, 脂肪重量: {data['BodyFatWeight']}, 脂肪指數: {data['BodyFatIndex']}, 脂肪百分比: {data['BodyFatPercentage']}, 基礎代謝率: {data['BasalMetabolicRate']}, 體水份: {data['BodyWater']}, 左手肌肉質量: {data['LeftHandMuscleMass']}, 右手肌肉質量: {data['RightHandMuscleMass']}, 左腿肌肉質量: {data['LeftLegMuscleMass']}, 右腿肌肉質量: {data['RightLegMuscleMass']}, 軀幹肌肉質量: {data['TrunkMuscleMass']}"
    
    # Send message with the formatted data string
    result = chat.send_message(data_str)
    
    # Generate a workout menu based on the advice
    result = chat.send_message("請幫忙設計一個適合的訓練菜單，動作名稱、組數、每組做多少次請詳細說明。只需提供訓練菜單，不用提供飲食建議，用Markdown格式輸出。")
    return result.text

def load_and_process_image(image_path):
    if "http" in image_path:
        image_path = image_utils.get_file(origin=image_path)
    print("Original image shape: ", mpimg.imread(image_path).shape)
    image_s = image_utils.load_img(image_path, target_size=(224, 224))
    image_s_array = image_utils.img_to_array(image_s)
    print("image_s_array shape: ", image_s_array.shape)
    image_s_array_reshape = image_s_array.reshape(1, 224, 224, 3)
    image_forVGG16 = preprocess_input(image_s_array_reshape)
    print("image_forVGG16 shape: ", image_forVGG16.shape)
    return image_forVGG16

def Posture():

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    classified_model = tf.keras.models.load_model('classified_model.h5')

    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360.0 - angle
            
        return angle

    # 讀取圖片
    img_cv = cv2.imread('static/tmp.jpg')
    img_class = load_and_process_image('static/tmp.jpg')

    if img_cv is None:
        print("Cannot read image")
        exit()

    # 轉換圖片顏色空間
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    # 等比例縮放圖片
    resize_factor = 1.2
    new_width = int(img_cv.shape[1] * resize_factor)
    new_height = int(img_cv.shape[0] * resize_factor)
    img_cv = cv2.resize(img_cv, (new_width, new_height))

    # 啟用姿勢偵測
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        results = pose.process(img_cv)
            
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # 獲取關鍵點座標
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
            foot = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]

            # 計算角度
            elbow_angle = calculate_angle(shoulder, elbow, wrist)
            shoulder_angle = calculate_angle(elbow, shoulder, hip)
            hip_angle = calculate_angle(shoulder, hip, knee)
            knee_angle = calculate_angle(hip, knee, ankle)
            foot_angle = calculate_angle(knee, ankle, foot)

            # 繪製姿勢骨架和關鍵點
            mp_drawing.draw_landmarks(
                img_cv,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            # 判斷姿勢是否標準
            ActType = classified_model.predict(img_class).argmax()
            if ActType == 1:
                cv2.putText(img_cv, 'Action Type:Squat', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                Posture_model = tf.keras.models.load_model('squat_model.h5')
                angle = np.array([hip_angle, knee_angle, foot_angle]).reshape(1, -1)
                prediction = Posture_model.predict(angle)
                if prediction > 0.5:
                    cv2.putText(img_cv, 'Position Correct', (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img_cv, 'Position Incorrect', (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            elif ActType == 0:
                cv2.putText(img_cv, 'Action Type:Row', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                Posture_model = tf.keras.models.load_model('Row_model.h5')
                angle = np.array([elbow_angle, shoulder_angle, hip_angle, knee_angle, foot_angle]).reshape(1, -1)
                prediction = Posture_model.predict(angle)
                if prediction > 0.5:
                    cv2.putText(img_cv, 'Position Correct', (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img_cv, 'Position Incorrect', (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(img_cv, 'Action Type:無法辨識', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imwrite('static/Show.jpg', cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    app.run(debug=True)
# import modules
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
    video = None
    photo = None

    if form.validate_on_submit():
        video = form.video.data
        photo = form.photo.data
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join('static', photo_filename))
        flash('Files uploaded successfully', 'success')        
        return render_template('photo.html',form = form,photo=photo_filename)  # Redirect to the same page after successful submission
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
    result = chat.send_message("你是一個健身教練，只能夠回答關於健身的問題，若問題跟健身無關請回答:我無法回答。不提供飲食建議。禁止使用簡體中文，有礙觀瞻。")
    result = chat.send_message("現在有一個身體數據，請問你能幫忙分析嗎？要減脂還是增肌？上下肢哪裡需要加強？需要增強哪些肌肉？")
    
    # Convert data to a format suitable for send_message
    data_str = f"性別: {data['Gender']}, 年齡: {data['Age']}, 身高: {data['Height']}, 體重: {data['Weight']}, 骨骼肌重量: {data['SkeletalMuscleWeight']}, 脂肪重量: {data['BodyFatWeight']}, 脂肪指數: {data['BodyFatIndex']}, 脂肪百分比: {data['BodyFatPercentage']}, 基礎代謝率: {data['BasalMetabolicRate']}, 體水份: {data['BodyWater']}, 左手肌肉質量: {data['LeftHandMuscleMass']}, 右手肌肉質量: {data['RightHandMuscleMass']}, 左腿肌肉質量: {data['LeftLegMuscleMass']}, 右腿肌肉質量: {data['RightLegMuscleMass']}, 軀幹肌肉質量: {data['TrunkMuscleMass']}"
    
    # Send message with the formatted data string
    result = chat.send_message(data_str)
    
    # Generate a workout menu based on the advice
    result = chat.send_message("請幫忙設計一個適合的訓練菜單，動作名稱、組數、每組做多少次請詳細說明。只需提供訓練菜單，不用提供飲食建議，用Markdown格式輸出。")
    return result.text


if __name__ == '__main__':
    app.run(debug=True)
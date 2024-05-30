# import modules
from flask import Flask, render_template, flash, redirect, url_for, request
from form import TrainingForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/css')
def index():
    return render_template('css.html')
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/', methods=['POST', 'GET'])
def home():
    form = TrainingForm()
    data = None  # 初始化 data 為 None
    if form.validate_on_submit():
        data = {
            'height': form.height.data,
            'weight': form.weight.data,
            'body_part': form.body_part.data,
            'video': form.video.data,
            'photo': form.photo.data,
            'additional_info': form.additional_info.data
        }
        flash('Data Submitted Successfully', 'success')
        return render_template('home.html', form=form, data=data)
    return render_template('home.html', form=form, data=data)


if __name__ == '__main__':
    app.run(debug=True)
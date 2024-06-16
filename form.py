from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, FloatField, FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class TrainingForm(FlaskForm):
    Gender = SelectField('性別', choices=[('Male', '男'), ('Female', '女')], validators=[DataRequired()])
    Age = IntegerField('年齡', validators=[DataRequired(), NumberRange(min=12, max=65)])
    Height = FloatField('身高 (cm)', validators=[DataRequired(), NumberRange(min=140, max=210)])
    Weight = FloatField('體重 (kg)', validators=[DataRequired(), NumberRange(min=40, max=150)])
    SkeletalMuscleWeight = FloatField('骨骼肌重 (kg)', validators=[DataRequired(), NumberRange(min=10, max=70)])
    BodyFatWeight = FloatField('脂肪重量 (kg)', validators=[DataRequired(), NumberRange(min=3, max=50)])
    BodyFatIndex = FloatField('體脂指數', validators=[DataRequired(), NumberRange(min=10, max=60)])
    BodyFatPercentage = FloatField('體脂率 (%)', validators=[DataRequired(), NumberRange(min=5, max=60)])
    BasalMetabolicRate = FloatField('基礎代謝率 (kcal/day)', validators=[DataRequired(), NumberRange(min=800, max=3000)])
    BodyWater = FloatField('體水份 (%)', validators=[DataRequired(), NumberRange(min=40, max=80)])
    LeftHandMuscleMass = FloatField('左手肌肉質量 (kg)', validators=[DataRequired(), NumberRange(min=0.5, max=5)])
    RightHandMuscleMass = FloatField('右手肌肉質量 (kg)', validators=[DataRequired(), NumberRange(min=0.5, max=5)])
    LeftLegMuscleMass = FloatField('左腿肌肉質量 (kg)', validators=[DataRequired(), NumberRange(min=3, max=15)])
    RightLegMuscleMass = FloatField('右腿肌肉質量 (kg)', validators=[DataRequired(), NumberRange(min=3, max=15)])
    TrunkMuscleMass = FloatField('軀幹肌肉質量 (kg)', validators=[DataRequired(), NumberRange(min=10, max=60)])
    submit = SubmitField('提交')

class PhotoForm(FlaskForm):
    # video = FileField('影片', validators=[DataRequired()])
    photo = FileField('照片', validators=[DataRequired()])
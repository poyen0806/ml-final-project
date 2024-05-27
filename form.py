from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField, TextAreaField
from wtforms.validators import DataRequired

class TrainingForm(FlaskForm):
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight')
    body_part = StringField('Body Part to Train')
    video = FileField('Video')
    photo = FileField('Photo' )
    additional_info = TextAreaField('Additional Info')
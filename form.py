from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, FloatField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class TrainingForm(FlaskForm):
    # height = FloatField('Height', validators=[DataRequired()])
    body_part = StringField('Body Part to Train')
    video = FileField('Video')
    photo = FileField('Photo' )
    additional_info = TextAreaField('Additional Info')

      
    Gender = SelectField('Gender', choices=['Male', 'Female'], validators=[DataRequired()])
    Age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=12, max=65)])
    Height = FloatField('Height (cm)', validators=[DataRequired(), NumberRange(min=150, max=190)])
    Weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=50, max=100)])
    SkeletalMuscleWeight = FloatField('Skeletal Muscle Weight (kg)', validators=[DataRequired(), NumberRange(min=20, max=50)])
    BodyFatWeight = FloatField('Body Fat Weight (kg)', validators=[DataRequired(), NumberRange(min=5, max=20)])
    BodyFatIndex = FloatField('Body Fat Index', validators=[DataRequired(), NumberRange(min=10, max=40)])
    BodyFatPercentage = FloatField('Body Fat Percentage (%)', validators=[DataRequired(), NumberRange(min=10, max=40)])
    BasalMetabolicRate = FloatField('Basal Metabolic Rate', validators=[DataRequired(), NumberRange(min=1000, max=2000)])
    BodyWater = FloatField('Body Water (%)', validators=[DataRequired(), NumberRange(min=50, max=70)])
    LeftHandMuscleMass = FloatField('Left Hand Muscle Mass (kg)', validators=[DataRequired(), NumberRange(min=1, max=4)])
    RightHandMuscleMass = FloatField('Right Hand Muscle Mass (kg)', validators=[DataRequired(), NumberRange(min=1, max=4)])
    LeftLegMuscleMass = FloatField('Left Leg Muscle Mass (kg)', validators=[DataRequired(), NumberRange(min=5, max=12)])
    RightLegMuscleMass = FloatField('Right Leg Muscle Mass (kg)', validators=[DataRequired(), NumberRange(min=5, max=12)])
    TrunkMuscleMass = FloatField('Trunk Muscle Mass (kg)', validators=[DataRequired(), NumberRange(min=20, max=50)])
    submit = SubmitField('Submit')
    
class PhotoForm(FlaskForm):
    video = FileField('Video', validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired()])

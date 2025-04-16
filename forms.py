from flask_wtf import FlaskForm # type: ignore
from wtforms.validators import DataRequired # type: ignore
from flask_wtf.file import FileAllowed # type: ignore
import wtforms as w # type: ignore



class UpdateProfileForm(FlaskForm):
    pfp = w.FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'gif'])])
    name = w.StringField('Display Name')
    accountname = w.StringField('Account Name', validators=[DataRequired()])
    location = w.StringField('Location')
    bio = w.TextAreaField('Biography')
    banner_color = w.ColorField('Banner Colour', validators=[DataRequired()])
    savebutton = w.SubmitField('Save')
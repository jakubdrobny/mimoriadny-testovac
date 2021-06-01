from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FieldList, SubmitField, FormField, SelectField
from wtforms.validators import DataRequired, ValidationError
import sys

class SubmitTaskForm(FlaskForm):
    # code = FileField('Kód', validators=[FileAllowed(['py', 'cpp'])])
    code = FileField('Kód', validators=[FileAllowed(['py'])])
    # language = SelectField('Jazyk', choices=[('def', '?'), ('py', 'Python 3.6'), ('cpp', 'GNU C++17')], default="def")
    language = SelectField('Jazyk', choices=[('def', '?'), ('py', 'Python 3.6')], default="def")
    submit = SubmitField('Odovzdať')

    def validate_language(self, language):
        if language.data == 'def':
            raise ValidationError('Prosím zvoľ si jazyk')
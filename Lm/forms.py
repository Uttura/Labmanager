from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Optional
from Lm.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password', message="Password must match.")])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')
class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')
class LabForm(FlaskForm):
    name = StringField('Lab Name', validators=[DataRequired()])
    platform = SelectField('Platform', validators=[DataRequired()], choices=[('Hack The Box', 'Hack The Box'), ('Try Hack Me', 'Try Hack Me'), ('Port Swigger', 'Port Swigger'),('Other', 'Other')])
    other_platform = StringField('Other Platform', validators=[Optional()])
    os = SelectField('Os',validators=[Optional()], choices=[('Windows', 'Windows'), ('Linux', 'Linux'), ('Mac', 'Mac Os'),('Other', 'Other')])
    other_os = StringField('Other Os', validators=[Optional()])
    difficulty = SelectField('Difficulty',validators=[Optional()], choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    ip_address = StringField('Ip_address',validators=[Optional()])
    notes = TextAreaField('Notes',validators=[Optional()])
    url = StringField('Url',validators=[Optional()])
    submit = SubmitField('Add Lab')

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
class FlagForm(FlaskForm):
    flag_value = StringField('Flag',validators=[DataRequired()])
    flag_type = SelectField('Flag Type',validate_choice=[DataRequired()], choices=[('Root', 'Root'), ('User','User'), ('Other','Other')])
    submit = SubmitField('Add_Flag')
class GithubForm(FlaskForm):
    github_owner=StringField('Github Owner')
    github_repo=StringField('Github Repo')
    github_path=StringField('Github Path')
    github_token=PasswordField('Github Token')
    submit = SubmitField("Connect Github", name='submit_github')
class ProfileForm(FlaskForm):
    username = StringField("Username",validators=[Optional()])
    email = StringField("Email",validators=[Email(),Optional()])
    password = PasswordField("Password",validators=[Optional()])
    confirm_password = PasswordField("Confirm Password",validators=[Optional(),EqualTo('password',message="Password must match.")])
    submit = SubmitField("Update", name='submit_profile')
    def __init__(self,user_id,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.user_id=user_id
    def validate_username(self, username):
        if username.data:
            user = User.query.filter(User.username == username.data, User.id != self.user_id).first()
            if user:
                raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        if email.data:
            user = User.query.filter(User.email == email.data, User.id != self.user_id).first()
            if user:
                raise ValidationError('Email is already registered.')
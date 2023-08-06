from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    ValidationError
    )
from supextend.models.owners import Owner


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                             DataRequired(),
                                             EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        owner = Owner.query.filter_by(username=username.data).first()
        if owner and owner.password:
            raise ValidationError('That username is taken. '
                                  'Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PasswordRegistrationForm(FlaskForm):
    username = StringField('Username',
                           render_kw={'disabled': ''})
    first_name = StringField('First Name',
                             render_kw={'disabled': ''})
    last_name = StringField('Last Name',
                            render_kw={'disabled': ''})

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                             DataRequired(),
                                             EqualTo('password')])
    submit = SubmitField('Register Password')

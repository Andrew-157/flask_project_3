import re

from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo, Email
from werkzeug.security import check_password_hash
from sqlalchemy import select


from .. import db
from ..models import User
from .crud import get_user_with_username, get_user_with_email


class RegisterForm(FlaskForm):
    username = StringField(label='Username*', validators=[InputRequired(),
                                                          Length(min=5, max=255)])
    email = EmailField(label='Email*', validators=[InputRequired(),
                                                   Length(max=255),
                                                   Email(message='Invalid email address.')])
    password1 = PasswordField(label='Password*', validators=[InputRequired(),
                                                             Length(min=8, max=255)])
    password2 = PasswordField(label='Password Confirmation*',
                              validators=[InputRequired(),
                                          Length(min=8, max=255),
                                          EqualTo('password1', message='Passwords did not match.')])

    def validate_username(self, field):
        user_with_username = get_user_with_username(username=field.data)
        if user_with_username:
            raise ValidationError(
                message='This username is already taken.'
            )
        allowed_symbols = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@.+-_"
        for symbol in field.data:
            if symbol not in allowed_symbols:
                raise ValidationError(
                    message='Username is not valid. Letters, digits and @/./+/-/_ only.'
                )

    def validate_email(self, field):
        user_with_email = get_user_with_email(email=field.data)
        if user_with_email:
            raise ValidationError(
                message='This email is already taken.'
            )


class LoginForm(FlaskForm):
    username = StringField(label='Username*', validators=[InputRequired(),
                                                          Length(min=5, max=255)])
    password = PasswordField(label='Password*', validators=[InputRequired(),
                                                            Length(min=5, max=255)])

    def validate_username(self, field):
        user_with_username = get_user_with_username(username=field.data)
        if not user_with_username:
            raise ValidationError('This username was not found.')

    def validate_password(self, field):
        user_with_username = get_user_with_username(
            username=self.username.data)
        if not check_password_hash(user_with_username.hashed_password, field.data):
            raise ValidationError('Wrong password.')


class UpdateUserForm(RegisterForm):
    password1 = None
    password2 = None

    def validate_username(self, field):
        current_user = g.user
        user_with_username = get_user_with_username(username=field.data)
        if user_with_username and (user_with_username != current_user):
            raise ValidationError(message='This username is already taken.')
        allowed_symbols = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@.+-_'
        for symbol in field.data:
            if symbol not in allowed_symbols:
                raise ValidationError(
                    message='Username is not valid. Letters, digits and @/./+/-/_ only.')

    def validate_email(self, field):
        current_user = g.user
        user_with_email = get_user_with_email(email=field.data)
        if user_with_email and (user_with_email != current_user):
            raise ValidationError(message='This email is already taken.')

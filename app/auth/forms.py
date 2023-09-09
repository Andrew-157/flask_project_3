import re

from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo, Email
from werkzeug.security import check_password_hash
from sqlalchemy import select


from .. import db
from ..models import User

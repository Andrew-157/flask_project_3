
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from config import config


class Base(DeclarativeBase):
    pass


def create_app(config_name: str = 'production'):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])

    return app

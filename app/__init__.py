
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

from config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(metadata=Base.metadata)
migrate = Migrate()


def create_app(config_name: str = 'production'):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    from .import models

    db.init_app(app)
    migrate.init_app(app=app, db=db)

    return app

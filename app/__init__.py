import functools

from flask import Flask, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from jinja2_pluralize import pluralize_dj

from config import config


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.become_user'))
        return view(**kwargs)
    return wrapped_view


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(metadata=Base.metadata)
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name: str = 'production'):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    from .import models
    from .auth.urls import bp as auth_bp
    from .main.urls import bp as main_bp

    db.init_app(app)
    migrate.init_app(app=app, db=db)

    app.jinja_env.filters['pluralize'] = pluralize_dj

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    csrf.init_app(app)

    return app

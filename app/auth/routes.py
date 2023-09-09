from flask import Blueprint
from flask import g
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from .. import db, login_required
from ..models import User
from .forms import RegisterForm, LoginForm, UpdateUserForm
from .crud import get_user_with_username, get_user_with_email


bp = Blueprint(name='auth',
               import_name=__name__,
               url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)


class RegisterView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self.form_class = RegisterForm
        self.template_name = 'auth/register.html'
        self.success_message = 'You successfully registered.'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form_class(formdata=request.form)
        if form.validate_on_submit():
            new_user = User(username=form.username.data,
                            email=form.email.data,
                            hashed_password=generate_password_hash(password=form.password1.data))
            db.session.add(new_user)
            db.session.commit()
            session.clear()
            session['user_id'] = new_user.id
            flash(message=self.success_message,
                  category='success')
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)


class LoginView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self.form_class = LoginForm
        self.template_name = 'auth/login.html'
        self.success_message = 'You successfully logged in.'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form_class(formdata=request.form)
        if form.validate_on_submit():
            user = get_user_with_username(username=form.username.data)
            session['user_id'] = user.id
            flash(message=self.success_message,
                  category='success')
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)


@bp.route(rule='/logout/', methods=['GET'])
def logout():
    session.clear()
    flash(message='You successfully logged out.',
          category='success')
    return redirect(url_for('main.index'))


class UpdateUserView(MethodView):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self) -> None:
        self.from_class = UpdateUserForm
        self.template_name = 'auth/update_user.html'
        self.success_message = 'You successfully updated your profile.'

    def get(self):
        current_user: User = g.user
        form = UpdateUserForm(username=current_user.username,
                              email=current_user.email)
        return render_template(self.template_name, form=form)

    def post(self):
        current_user: User = g.user
        form = UpdateUserForm(formdata=request.form)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.add(current_user)
            db.session.commit()
            flash(self.success_message, category='success')
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)


@bp.route(rule='/authenticate/', methods=['GET'])
def become_user():
    return render_template('auth/become_user.html')

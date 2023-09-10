from flask import Blueprint
from flask import render_template

from .. import login_required

bp = Blueprint(name='main',
               import_name=__name__)


@bp.route(rule='/', methods=['GET'])
def index():
    return render_template('main/index.html')


@bp.route('/you/', methods=['GET'])
@login_required
def private_page():
    return render_template('main/private_page.html')

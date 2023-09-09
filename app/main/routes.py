from flask import Blueprint
from flask import render_template


bp = Blueprint(name='main',
               import_name=__name__)


@bp.route(rule='/', methods=['GET'])
def index():
    return render_template('main/index.html')

from .routes import bp
from .routes import RegisterView, LoginView, UpdateUserView


bp.add_url_rule(rule='/register/',
                view_func=RegisterView.as_view(name='register'))
bp.add_url_rule(rule='/login/',
                view_func=LoginView.as_view(name='login'))
bp.add_url_rule(
    rule='/update/', view_func=UpdateUserView.as_view(name='update_user'))

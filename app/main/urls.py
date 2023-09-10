from .routes import bp
from . import routes

bp.add_url_rule(
    rule='/recommend/',
    view_func=routes.PostRecommendationView.as_view(name='post_recommendation')
)

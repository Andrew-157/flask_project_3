from .routes import bp
from . import routes

bp.add_url_rule(
    rule='/recommend/',
    view_func=routes.PostRecommendationView.as_view(name='post_recommendation')
)
bp.add_url_rule(
    rule='/recommendations/<int:id>/update/',
    view_func=routes.UpdateRecommendationView.as_view(
        name='update_recommendation')
)
bp.add_url_rule(
    rule='/recommendations/<int:id>/delete/',
    view_func=routes.DeleteRecommendationView.as_view(
        name='delete_recommendation')
)

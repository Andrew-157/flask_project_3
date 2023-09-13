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
bp.add_url_rule(
    rule='/recommendations/<int:id>/like/',
    view_func=routes.LeavePositiveReactionView.as_view(
        name='like_recommendation')
)
bp.add_url_rule(
    rule='/recommendations/<int:id>/dislike/',
    view_func=routes.LeaveNegativeReactionView.as_view(
        name='dislike_recommendation')
)
bp.add_url_rule(
    rule='/recommendations/<int:id>/saved/',
    view_func=routes.AddRemoveSavedRecommendation.as_view(
        name='save_unsave_recommendation')
)
bp.add_url_rule(
    rule='/recommendations/<int:id>/comment/',
    view_func=routes.PostCommentView.as_view(name='comment_recommendation')
)

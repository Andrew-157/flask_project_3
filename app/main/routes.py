from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for
from flask import g
from flask import abort
from flask import request
from flask.views import MethodView

from .. import login_required, db
from ..models import User, FictionType, Tag, Recommendation, Reaction, Comment
from .forms import PostUpdateRecommendationForm, PostUpdateCommentForm
from .crud import get_fiction_type_by_name, get_tag_by_name, get_recommendation_by_id,\
    get_reaction_by_user_id_and_recommendation_id, count_positive_reactions_for_recommendation,\
    count_negative_reactions_for_recommendation

bp = Blueprint(name='main',
               import_name=__name__)


@bp.route(rule='/', methods=['GET'])
def index():
    a = 'string'
    return render_template('main/index.html', a=a)


@bp.route('/you/', methods=['GET'])
@login_required
def private_page():
    return render_template('main/private_page.html')


class PostRecommendationView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self.form_class = PostUpdateRecommendationForm
        self.template_name = 'main/post_recommendation.html'
        self.success_message = 'You successfully posted new recommendation!'
        self.info_message = 'Please, login or register to post a recommendation.'

    def get_fiction_type_object(self, fiction_type_name: str) -> FictionType:
        fiction_type_name = fiction_type_name.strip().lower()
        fiction_type_object = get_fiction_type_by_name(name=fiction_type_name)
        if fiction_type_object:
            return fiction_type_object
        else:
            fiction_type_slug = fiction_type_name.replace(' ', '-')
            fiction_type_object = FictionType(name=fiction_type_name,
                                              slug=fiction_type_slug)
            return fiction_type_object

    def get_tags_objects(self, tags: str) -> list[Tag]:
        tags = tags.strip()
        splitted_tags = tags.split(',')
        tags_str_list = []
        for tag in splitted_tags:
            if not tag:
                pass
            elif tag.isspace():
                pass
            else:
                tags_str_list.append(tag.strip().lower().replace(' ', '-'))

        tags_obj_list = []
        for tag in tags_str_list:
            tag_object = get_tag_by_name(name=tag)
            if not tag_object:
                tag_object = Tag(name=tag)
                tags_obj_list.append(tag_object)
            else:
                tags_obj_list.append(tag_object)

        return tags_obj_list

    def get(self):
        current_user: User | None = g.user
        if not current_user:
            flash(message=self.info_message, category='info')
            return redirect(url_for('main.index'))
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        current_user: User | None = g.user
        if not current_user:
            flash(message=self.info_message, category='info')
            return redirect(url_for('main.index'))
        form = self.form_class(formdata=request.form)
        if form.validate_on_submit():
            fiction_type = self.get_fiction_type_object(
                fiction_type_name=form.fiction_type.data)
            new_recommendation = Recommendation(
                fiction_type=fiction_type,
                title=form.title.data,
                short_description=form.short_description.data,
                opinion=form.opinion.data,
                user_id=current_user.id
            )
            tags = self.get_tags_objects(tags=form.tags.data)
            new_recommendation.tags = tags
            db.session.add(fiction_type)
            db.session.add(new_recommendation)
            db.session.commit()
            flash(self.success_message,
                  category='success')
            return redirect(url_for('main.recommendation_detail',
                                    id=new_recommendation.id))
        return render_template(self.template_name,
                               form=form)


@bp.route('/recommendations/<int:id>/', methods=['GET'])
def recommendation_detail(id):
    recommendation = get_recommendation_by_id(id=id)
    if not recommendation:
        abort(404)
    reaction = None
    current_user: User | None = g.user
    if current_user:
        reaction = get_reaction_by_user_id_and_recommendation_id(user_id=current_user.id,
                                                                 recommendation_id=recommendation.id)
    positive_reactions = count_positive_reactions_for_recommendation(
        recommendation_id=recommendation.id)
    negative_reactions = count_negative_reactions_for_recommendation(
        recommendation_id=recommendation.id)
    return render_template('main/recommendation_detail.html',
                           recommendation=recommendation,
                           reaction=reaction,
                           positive_reactions=positive_reactions,
                           negative_reactions=negative_reactions)


class UpdateRecommendationView(MethodView):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self) -> None:
        self.form_class = PostUpdateRecommendationForm
        self.template_name = 'main/update_recommendation.html'
        self.success_message = 'You successfully updated your recommendation!'

    def get_fiction_type_object(self, fiction_type_name: str) -> FictionType:
        fiction_type_name = fiction_type_name.strip().lower()
        fiction_type_object = get_fiction_type_by_name(name=fiction_type_name)
        if fiction_type_object:
            return fiction_type_object
        else:
            fiction_type_slug = fiction_type_name.replace(' ', '-')
            fiction_type_object = FictionType(name=fiction_type_name,
                                              slug=fiction_type_slug)
            return fiction_type_object

    def get_tags_objects(self, tags: str) -> list[Tag]:
        tags = tags.strip()
        splitted_tags = tags.split(',')
        tags_str_list = []
        for tag in splitted_tags:
            if not tag:
                pass
            elif tag.isspace():
                pass
            else:
                tags_str_list.append(tag.strip().lower().replace(' ', '-'))

        tags_obj_list = []
        for tag in tags_str_list:
            tag_object = get_tag_by_name(name=tag)
            if not tag_object:
                tag_object = Tag(name=tag)
                tags_obj_list.append(tag_object)
            else:
                tags_obj_list.append(tag_object)

        return tags_obj_list

    def get(self, id: int):
        current_user: User = g.user
        recommendation = get_recommendation_by_id(id=id)
        if not recommendation:
            abort(404)
        if recommendation.user != current_user:
            abort(403)
        tags = ', '.join([tag.name for tag in recommendation.tags])
        form = self.form_class(
            fiction_type=recommendation.fiction_type.name.capitalize(),
            title=recommendation.title,
            short_description=recommendation.short_description,
            opinion=recommendation.opinion,
            tags=tags)
        return render_template(self.template_name, form=form,
                               recommendation=recommendation)

    def post(self, id: int):
        current_user: User = g.user
        recommendation = get_recommendation_by_id(id=id)
        if not recommendation:
            abort(404)
        if recommendation.user != current_user:
            abort(403)
        form = self.form_class(formdata=request.form)
        if form.validate_on_submit():
            fiction_type = self.get_fiction_type_object(
                fiction_type_name=form.fiction_type.data)
            recommendation.fiction_type = fiction_type
            recommendation.title = form.title.data
            recommendation.short_description = form.short_description.data
            recommendation.opinion = form.opinion.data
            tags = self.get_tags_objects(tags=form.tags.data)
            recommendation.tags = tags
            recommendation.updated = datetime.utcnow()
            db.session.add(recommendation)
            db.session.commit()
            flash(message=self.success_message,
                  category='success')
            return redirect(url_for('main.recommendation_detail',
                                    id=id))
        return render_template(self.template_name,
                               form=form,
                               recommendation=recommendation)


class DeleteRecommendationView(MethodView):
    methods = ['POST']
    decorators = [login_required]

    def post(self, id: int):
        current_user: User = g.user
        recommendation = db.session.get(Recommendation, id)
        if not recommendation:
            abort(404)
        if recommendation.user != current_user:
            abort(403)
        db.session.delete(recommendation)
        db.session.commit()
        flash(message='You successfully deleted your recommendation.',
              category='success')
        return redirect(url_for('main.index'))


class LeaveReactionBaseView(MethodView):
    is_positive = None
    methods = ['POST']

    def get_redirect_url(self):
        return redirect(url_for('main.recommendation_detail',
                                id=self.recommendation.id))

    def post(self, id):
        current_user: User | None = g.user
        recommendation = db.session.get(Recommendation, id)
        if not recommendation:
            abort(404)
        self.recommendation = recommendation
        if not current_user:
            flash(message='Please, login or register to leave your reaction about the recommendation.',
                  category='info')
            return self.get_redirect_url()
        reaction = get_reaction_by_user_id_and_recommendation_id(
            user_id=current_user.id,
            recommendation_id=recommendation.id)
        if self.is_positive == False:
            if not reaction:
                reaction = Reaction(
                    is_positive=False,
                    user_id=current_user.id,
                    recommendation_id=recommendation.id
                )
                db.session.add(reaction)
                db.session.commit()
            else:
                if reaction.is_positive == True:
                    reaction.is_positive = False
                    db.session.add(reaction)
                    db.session.commit()
                elif reaction.is_positive == False:
                    db.session.delete(reaction)
                    db.session.commit()
        if self.is_positive == True:
            if not reaction:
                reaction = Reaction(
                    is_positive=True,
                    user_id=current_user.id,
                    recommendation_id=recommendation.id
                )
                db.session.add(reaction)
                db.session.commit()
            else:
                if reaction.is_positive == False:
                    reaction.is_positive = True
                    db.session.add(reaction)
                    db.session.commit()
                elif reaction.is_positive == True:
                    db.session.delete(reaction)
                    db.session.commit()

        return self.get_redirect_url()


class LeavePositiveReactionView(LeaveReactionBaseView):
    is_positive = True


class LeaveNegativeReactionView(LeaveReactionBaseView):
    is_positive = False


class AddRemoveSavedRecommendation(MethodView):
    methods = ['POST']

    def get_redirect_url(self):
        return redirect(url_for('main.recommendation_detail',
                                id=self.recommendation.id))

    def post(self, id):
        current_user: User | None = g.user
        recommendation = db.session.get(Recommendation, id)
        if not recommendation:
            abort(404)
        self.recommendation = recommendation
        if not current_user:
            flash(
                message='Please, login or register to save this recommendation.', category='info')
            return self.get_redirect_url()
        if recommendation in current_user.saved_recommendations:
            current_user.saved_recommendations.remove(recommendation)
            db.session.add(current_user)
            db.session.commit()
            flash(message='You removed this recommendation from the saved.',
                  category='success')
        else:
            current_user.saved_recommendations.append(recommendation)
            db.session.add(current_user)
            db.session.commit()
            flash(message='You saved this recommendation.', category='success')
        return self.get_redirect_url()


class PostCommentView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self):
        self.form_class = PostUpdateCommentForm
        self.template_name = 'main/post_comment.html'
        self.success_message = 'You successfully commented this recommendation.'
        self.info_message = 'Please, login or register to comment the recommendation.'

    def get(self, id):
        recommendation = db.session.get(Recommendation, id)
        if not recommendation:
            abort(404)
        current_user: User | None = g.user
        if not current_user:
            flash(message=self.info_message,
                  category='info')
            return redirect(url_for('main.recommendation_detail', id=recommendation.id))
        form = self.form_class()
        return render_template(self.template_name,
                               form=form,
                               recommendation=recommendation)

    def post(self, id):
        recommendation = db.session.get(Recommendation, id)
        if not recommendation:
            abort(404)
        current_user: User | None = g.user
        if not current_user:
            flash(message=self.info_message,
                  category='info')
            return redirect(url_for('main.recommendation_id', id=recommendation.id))
        form = self.form_class(formdata=request.form)
        if form.validate_on_submit():
            new_comment = Comment(
                body=form.body.data,
                user_id=current_user.id,
                recommendation_id=recommendation.id)
            db.session.add(new_comment)
            db.session.commit()
            flash(message=self.success_message,
                  category='success')
            return redirect(url_for('main.recommendation_detail',
                                    id=recommendation.id))
        return render_template(self.template_name,
                               form=form,
                               recommendation=recommendation)

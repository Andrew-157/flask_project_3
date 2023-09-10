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
from ..models import User, FictionType, Tag, Recommendation
from .forms import PostUpdateRecommendationForm
from .crud import get_fiction_type_by_name, get_tag_by_name, get_recommendation_by_id

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
    return render_template('main/recommendation_detail.html',
                           recommendation=recommendation)


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

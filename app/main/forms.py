from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length


class PostUpdateRecommendationForm(FlaskForm):
    fiction_type = StringField(label='Type of Fiction*',
                               validators=[InputRequired(),
                                           Length(min=3, max=255)],
                               description='For example: Movie.')
    title = StringField(label='Title*',
                        validators=[InputRequired(),
                                    Length(min=2, max=255)],
                        description='For example: Interstellar.')
    short_description = TextAreaField(label='Short Description*',
                                      validators=[InputRequired(),
                                                  Length(min=5)],
                                      description='For example: Sci-fi movie about space.')
    opinion = TextAreaField(label='Your Opinion*',
                            validators=[InputRequired(),
                                        Length(min=5)],
                            description='For example: My favorite movie.')
    tags = StringField(label='Tags',
                       description='Write tags, separating them with a comma. #-sign is unnecessary.')


class PostUpdateCommentForm(FlaskForm):
    body = TextAreaField(label='Your Comment*',
                         validators=[InputRequired(),
                                     Length(min=5)],
                         description='For example: Thank you for your recommendation!')

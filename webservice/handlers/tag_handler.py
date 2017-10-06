from flask import jsonify, request, g
from flask.views import MethodView

from webservice import app, db
from webservice.models.tag_model import Tag

class TagHanlder(MethodView):
    def get(self):
        tags = Tag.query.all()
        return 'Getting tags'

    def post(self):
        return 'Posting tags'


app.add_url_rule('/tags/', view_func=TagHanlder.as_view('tags'))

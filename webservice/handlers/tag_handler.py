from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException
from sqlalchemy.exc import IntegrityError

from webservice import app, db
from webservice.models.tag_model import Tag
from webservice.decorators.login_required import login_required

class TagHanlder(MethodView):
    @login_required
    def get(self):
        tags = Tag.query.all()

        return jsonify([tag.serialize for tag in tags])

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('label', type=str, required=True, help='Label is required')

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        req = request.json

        tag = Tag(label=req['label'], user_id=g.user.id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            return jsonify({'BAD_REQUEST': 'Label already taken'})

        return jsonify('ALL_OK'), 201


app.add_url_rule('/tags/', view_func=TagHanlder.as_view('tags'))

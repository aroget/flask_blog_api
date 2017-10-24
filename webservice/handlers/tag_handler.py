from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException
from sqlalchemy.exc import IntegrityError

from webservice import app, db
from webservice.models.tag_model import Tag
from webservice.decorators.login_required import login_required


FILTER_TYPE = {
    'active': 1,
    'inactive': 0
}


class TagHanlder(MethodView):
    @login_required
    def get(self, tag_id=None):
        filter_by_arg = request.args.get('filter')

        if tag_id is not None:
            tag = Tag.query.get(tag_id)


            if tag is None:
                return jsonify('NOT_FOUND'), 404

            not_owner = tag.user_id != g.user.id
            not_active = tag.is_active == False

            if not_owner or not_active:
                return jsonify('NOT_FOUND'), 404

        query = Tag.query
        query.filter(Tag.user_id==g.user.id)

        if filter_by_arg is not None:

            is_active_filter = FILTER_TYPE.get(filter_by_arg)

            if is_active_filter is not None:
                query = query.filter(Tag.is_active==is_active_filter)

        tags = query.all()

        return jsonify([tag.serialize for tag in tags])


    @login_required
    def delete(self, tag_id):
        tag = Tag.query.get(tag_id)

        if tag is None:
            return jsonify('NOT_FOUND'), 404

        if tag.user_id is not g.user.id:
            return jsonify('FORBIDDEN'), 403

        tag.is_active = False

        db.session.add(tag)
        db.session.commit()

        return jsonify('ALL_OK'), 200

    @login_required
    def put(self, tag_id):
        tag = Tag.query.get(tag_id)

        if tag is None:
            return jsonify('NOT_FOUND'), 404

        parser = reqparse.RequestParser()
        parser.add_argument('label', type=str, required=False)
        parser.add_argument('is_active', type=bool, required=False)


        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        if (args['label'] is not None):
            tag.label = args['label']

        if (args['is_active'] is not None):
            tag.is_active = args['is_active']


        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            return jsonify('BAD_REQUEST'), 400

        return jsonify('ALL_OK'), 200

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


tags_handler = TagHanlder.as_view('tags')

app.add_url_rule('/tags/', defaults={'tag_id': None},
                 view_func=tags_handler, methods=['GET',])

app.add_url_rule('/tags/', view_func=tags_handler, methods=['POST',])

app.add_url_rule('/tags/<int:tag_id>', view_func=tags_handler,
                 methods=['GET', 'PUT', 'DELETE'])

from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException
from sqlalchemy.exc import IntegrityError

from webservice import app, db
from webservice.models.tag_model import Tag
from webservice.decorators.login_required import login_required
from webservice.utils.handlers.register_handler import register_handler


ACTIVE_TYPE = {
    '1': 1,
    '0': 0
}

class TagHandler(MethodView):
    @login_required
    def get(self, tag_id=None):
        filter_by_arg = request.args.get('filter')

        if tag_id is not None:
            tag = Tag.query.get_or_404(tag_id)

            not_owner = tag.is_from_author(g.user.author.id)

            if not_owner or tag.is_active is not True:
                return jsonify('NOT_FOUND'), 404

            return jsonify({'response': tag.serialize})

        query = Tag.query
        query = query.filter(Tag.author_id==g.user.author.id)

        if filter_by_arg is not None:
            parser = reqparse.RequestParser()
            parser.add_argument('filter', choices=('1', '0'), location='args')

            try:
                args = parser.parse_args()
            except HTTPException as error:
                return jsonify({'BAD_REQUEST': error.data.get('message', '')})

            is_active_filter = ACTIVE_TYPE.get(filter_by_arg)

            if is_active_filter is not None:
                query = query.filter(Tag.is_active==is_active_filter)

        tags = query.all()

        return jsonify([tag.serialize for tag in tags])


    @login_required
    def delete(self, tag_id):
        tag = Tag.query.get_or_404(tag_id)

        if tag.author_id is not g.user.author.id:
            return jsonify('FORBIDDEN'), 403

        tag.is_active = False

        db.session.add(tag)
        db.session.commit()

        return jsonify('ALL_OK'), 200

    @login_required
    def put(self, tag_id):
        tag = Tag.query.get_or_404(tag_id)

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

register_handler(TagHandler, 'tags', '/tags/', pk='tag_id')

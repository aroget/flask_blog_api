from flask.views import MethodView
from flask import jsonify, request, g
from sqlalchemy.exc import IntegrityError
from flask_restful import reqparse, HTTPException

from webservice import app, db
from webservice.models.user_model import User
from webservice.decorators.login_required import login_required


class UserHanlder(MethodView):
    @login_required
    def get(self, user_id):
        return jsonify({'response': g.user.serialize})

    @login_required
    def put(self, user_id):
        user = User.query.get(g.user.id)

        if user is None:
            return jsonify('NOT_FOUND'), 404

        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        req = request.json

        if req['first_name']:
            user.first_name = req['first_name']

        if req['last_name']:
            user.last_name = req['last_name']

        if req['email']:
            user.email = req['email']

        db.session.add(tag)
        db.session.commit()

        return jsonify('ALL_OK'), 200


    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True, help='First name is required')
        parser.add_argument('last_name', type=str, required=True, help='Last name is required')
        parser.add_argument('user_name', type=str, required=True, help='User name is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', required=True, help='Password is required')

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        req = request.json
        user = User(first_name=req['first_name'], last_name=req['last_name'],
                    user_name=req['user_name'], email=req['email'],
                    password=req['password'])

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session().rollback()
            return jsonify({'BAD_REQUEST': 'User already exists'}), 400

        return jsonify({'ALL_OK': None})


user_handler = UserHanlder.as_view('users')

app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_handler, methods=['GET',])

app.add_url_rule('/users/', view_func=user_handler, methods=['POST',])

app.add_url_rule('/user/<int:user_id>', view_func=user_handler,
                 methods=['GET', 'PUT', 'DELETE'])

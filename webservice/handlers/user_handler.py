from flask.views import MethodView
from flask import jsonify, request, g
from sqlalchemy.exc import IntegrityError
from flask_restful import reqparse, HTTPException

from webservice import app, db
from webservice.models.user_model import User
from webservice.utils.email_utils import send_welcome_email
from webservice.decorators.login_required import login_required


class UserHanlder(MethodView):
    @login_required
    def get(self):
        to_name = "{} {}".format(g.user.first_name, g.user.last_name)

        send_welcome_email(to_email = g.user.email, to_name = to_name)
        return jsonify({'response': g.user.serialize})


    def post(self):
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

app.add_url_rule('/users/', view_func=UserHanlder.as_view('users'))

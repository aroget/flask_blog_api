from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException

from webservice import app, db
from webservice.models.user_model import User
from webservice.utils.access_token import create_token
from webservice.models.access_token_model import AccessToken

class SessionHanlder(MethodView):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str, required=True, help='User Name is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify('BAD_REQUEST'), 400

        req = request.json

        user = User.query.filter_by(user_name=req['user_name']).first()

        password_match = user.check_password(req['password'])

        if user is None or password_match is False:
            return jsonify('NO USER FOUND'), 400

        encoded_token = create_token(user)

        token = AccessToken(token=encoded_token, user_id=user.id)

        db.session.add(token)
        db.session.commit()

        return jsonify({'token': token.token}), 200


app.add_url_rule('/session/', view_func=SessionHanlder.as_view('session'))

from functools import wraps
from flask import g, request, jsonify

from webservice.models.user_model import User
from webservice.models.access_token_model import AccessToken

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').split()[1]
        except AttributeError:
            response = jsonify('Missing Header'), 400
            return response
        except IndexError:
            response = jsonify('Missing Token'), 400
            return response

        try:
            token = AccessToken.query.filter_by(token=token).first()
        except expression as identifier:
            return jsonify('Token not found'), 400

        user = User.query.get(token.user_id)

        if user is None:
            return jsonify('No User Found'), 400

        g.user = user

        return f(*args, **kwargs)
    return decorated_function

from functools import wraps
from flask import g, request, jsonify

from webservice.models.user_model import User

def author_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.get(g.user.id)

        if user.author is None:
            return jsonify('UNAUTHORIZED'), 403

        return f(*args, **kwargs)
    return decorated_function

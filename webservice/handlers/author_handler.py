from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException

from webservice import app, db
from webservice.models.author_model import Author, User
from webservice.decorators.login_required import login_required

class AuthorHandler(MethodView):
    @login_required
    def get(self):
        authors = Author.query.all()
        return jsonify({'response': [author.serialize for author in authors]})

    def post(self):
        req = request.json
        user_id = None

        parser = reqparse.RequestParser()

        if ('user_id' in req.keys()):
            user_id = req['user_id']
            parser.add_argument('user_id', type=int, required=True)
        else:
            parser.add_argument('first_name', type=str, required=True)
            parser.add_argument('last_name', type=str, required=True)
            parser.add_argument('user_name', type=str, required=True)
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('password', type=str, required=True)

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})


        if user_id is not None:
            user = User.query.get(user_id)

            if user is None:
                return jsonify('NOT FOUND'), 404

            author = Author(user_id=user_id, user=user)

            db.session.add(author)
            db.session.commit()

            return jsonify('ALL_OK'), 201

        else:
            req = request.json
            user = User(first_name=req['first_name'], last_name=req['last_name'],
                        user_name=req['user_name'], email=req['email'],
                        password=req['password'])

            db.session.add(user)

            author = Author(user_id=user.id, user=user)

            db.session.add(author)

            db.session.commit()

            return jsonify('ALL_OK'), 201


app.add_url_rule('/authors/', view_func=AuthorHandler.as_view('authors'))

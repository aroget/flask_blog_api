from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException

from webservice import app, db
from webservice.models.author_model import Author, User
from webservice.decorators.login_required import login_required

ACTIVE_TYPE = {
    '1': 1,
    '0': 0
}

class AuthorHandler(MethodView):
    @login_required
    def get(self, author_id):

        if author_id is not None:
            author = Author.query.get_or_404(author_id)
            return jsonify({'response': author.serialize})

        query = Author.query
        filter_by_arg = request.args.get('filter')

        if filter_by_arg is not None:
            parser = reqparse.RequestParser()
            parser.add_argument('filter', choices=('1', '0'), location='args')

            try:
                args = parser.parse_args()
            except HTTPException as error:
                return jsonify({'BAD_REQUEST': error.data.get('message', '')})

            query = query.filter(Author.is_active==ACTIVE_TYPE.get(filter_by_arg))

        authors = query.all()
        return jsonify({'response': [author.serialize for author in authors]})

    @login_required
    def post(self, author_id):
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


    @login_required
    def put(self, author_id):
        parser = reqparse.RequestParser()

        author = Author.query.get_or_404(author_id)

        parser.add_argument('is_active', type=bool, required=True)

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        author.is_active = args.get('is_active')

        if author.is_active is False:
            print('Should disable all posts from author')

        db.session.add(author)
        db.session.commit()

        return jsonify({'response': author.serialize}), 200



author_handler = AuthorHandler.as_view('authors')

app.add_url_rule('/authors/', defaults={'author_id': None},
                 view_func=author_handler, methods=['GET',])

app.add_url_rule('/authors/', view_func=author_handler, methods=['POST',])

app.add_url_rule('/authors/<int:author_id>', view_func=author_handler,
                 methods=['GET', 'PUT', 'DELETE'])

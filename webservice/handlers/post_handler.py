import datetime
from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException

from webservice import app, db, cache
from webservice.models.tag_model import Tag
from webservice.models.post_model import Post
from webservice.models.user_model import User
from webservice.models.author_model import Author
from webservice.decorators.login_required import login_required
from webservice.utils.handlers.register_handler import register_handler

class PostsLike(MethodView):
    @login_required
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)

        if post.is_draft:
            return jsonify('NOT_FOUND'), 404

        parser = reqparse.RequestParser()
        parser.add_argument('likes', type=str, required=True, choices=('1', '0'))

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        user = User.query.get_or_404(g.user.id)

        if args.likes == '1':
            user.likes.append(post)

        if args.likes == '0':
            user.likes.remove(post)

        db.session.add(post)
        db.session.add(user)
        db.session.commit()

        return jsonify({'response': post.serialize}), 200


register_handler(PostsLike, 'posts_like', '/posts/like/', pk='post_id')

class PostsByTag(MethodView):
    def get(self, tag_id):
        tag = Tag.query.get_or_404(tag_id)

        posts = Post.query.filter_by(tag_id=tag_id, is_private=False, is_published=True)

        return jsonify({'response': [post.serialize for post in posts]}), 200


register_handler(PostsByTag, 'posts_by_tag', '/posts/tag/', pk='tag_id')

class PostByAuthor(MethodView):
    def get(self, author_id):
        author = Author.query.get_or_404(author_id)

        posts = Post.query.filter_by(author_id=author_id, is_private=False, is_published=True)

        return jsonify({'response': [post.serialize for post in posts]}), 200


register_handler(PostByAuthor, 'posts_by_author', '/posts/author/', pk='author_id')

class PostHandler(MethodView):
    @cache.cached(timeout=500)
    def get(self, post_id):
        if post_id is not None:
            post = Post.query.get_or_404(post_id)
            return jsonify({'response': post.serialize}), 200

        posts = Post.query.all()
        return jsonify({'response': [post.serialize for post in posts]}), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('body', type=str, required=True)
        parser.add_argument('author_id', type=int, required=True)

        parser.add_argument('tag_id', type=int)
        parser.add_argument('is_draft', type=bool)
        parser.add_argument('is_private', type=bool)
        parser.add_argument('is_published', type=bool)
        parser.add_argument('feature_image', type=int)

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        author = Author.query.get_or_404(args.author_id)

        if author.is_active is False:
            return jsonify('BAD_REQUEST'), 400

        post = Post(title=args.title, body=args.body, author_id=args.author_id)

        if args.tag_id:
            post.tag_id = args.tag_id

        if args.is_private:
            post.is_private = args.is_private

        if args.is_draft:
            post.is_draft = args.is_draft

        if args.is_published:
            post.is_published = args.is_published
            post.published_date = datetime.datetime.now()

        if args.feature_image:
            post.feature_image = args.feature_image

        db.session.add(post)
        db.session.commit()

        return jsonify({'response': post.serialize}), 201

    @login_required
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('body', type=str, required=True)
        parser.add_argument('author_id', type=int, required=True)

        parser.add_argument('tag_id', type=int)
        parser.add_argument('is_draft', type=bool)
        parser.add_argument('is_private', type=bool)
        parser.add_argument('is_published', type=bool)
        parser.add_argument('feature_image', type=int)

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        author = Author.query.get_or_404(args.author_id)

        if author.is_active is False:
            return jsonify('BAD_REQUEST'), 400

        post = Post(title=args.title, body=args.body, author_id=args.author_id)

        if args.tag_id:
            post.tag_id = args.tag_id

        if args.is_private:
            post.is_private = args.is_private

        if args.is_draft:
            post.is_draft = args.is_draft

        if args.is_published:
            post.is_published = args.is_published
            post.published_date = datetime.datetime.now()

        if args.feature_image:
            post.feature_image = args.feature_image

        db.session.add(post)
        db.session.commit()

        return jsonify({'response': post.serialize}), 201

    @login_required
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)

        if post.is_author(g.user.author.id) is False:
            return jsonify('UNAUTHORIZED'), 403


register_handler(PostHandler, 'posts', '/posts/', pk='post_id')



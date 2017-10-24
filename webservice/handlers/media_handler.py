from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException

from webservice import app, db
from webservice.models.media_model import Media
from webservice.decorators.login_required import login_required
from webservice.decorators.author_access import author_access

class MediaHandler(MethodView):
    @login_required
    @author_access
    def get(self, media_id):

        if media_id is not None:
            media = Media.query.get_or_404(media_id)
            return jsonify({'response': media.serialize})

        media_list = Media.query.filter_by(author_id=g.user.author.id)
        return jsonify({'response': [media.serialize for media in media_list]})

    @login_required
    @author_access
    def post(self, media_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('url', type=str)
        parser.add_argument('media_type', type=str)

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})

        media = Media(name=args['name'], url=args['url'],
                      media_type=args['media_type'], author_id=g.user.author.id)

        db.session.add(media)
        db.session.commit()

        return jsonify('ALL_OK'), 201


media_handler = MediaHandler.as_view('media')

app.add_url_rule('/media/', defaults={'media_id': None},
                 view_func=media_handler, methods=['GET',])

app.add_url_rule('/media/', view_func=media_handler, methods=['POST',])

app.add_url_rule('/media/<int:media_id>', view_func=media_handler,
                 methods=['GET', 'PUT', 'DELETE'])

from flask import jsonify, request, g
from flask.views import MethodView
from flask_restful import reqparse, HTTPException

from webservice import app, db
from webservice.models.media_model import Media
from webservice.decorators.login_required import login_required

class MediaHandler(MethodView):
    @login_required
    def get(self):
        media_list = Media.query.filter_by(user_id=g.user.id)
        return jsonify({'response': [media.serialize for media in media_list]})

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('url', type=str)
        parser.add_argument('media_type', type=str)

        try:
            args = parser.parse_args()
        except HTTPException as error:
            return jsonify({'BAD_REQUEST': error.data.get('message', '')})


        # try:
        #     Media.supported(args['url'].split('.')[-1])
        # except ValueError as error:
        #     return jsonify('ERROR', error), 400

        media = Media(name=args['name'], url=args['url'],
                      media_type=args['media_type'], user_id=g.user.id)

        db.session.add(media)
        db.session.commit()

        return jsonify('ALL_OK'), 201


app.add_url_rule('/media/', view_func=MediaHandler.as_view('media'))

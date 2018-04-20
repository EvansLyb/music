# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api

from app.models import create_tables
from app.views import TestView, AlbumListView, AlbumView, ClassificationListView


app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

api.prefix = '/api/v1'
api.add_resource(TestView, '/test')
api.add_resource(AlbumListView, '/album')
api.add_resource(AlbumView, '/album/<album_id>')
api.add_resource(ClassificationListView, '/classification')


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=6999, use_reloader=False)

from flask_restful import Resource, reqparse, fields, marshal
from flask import make_response
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError

from app.models import Classification, Album, AlbumClassificationThrough

import json


class TestView(Resource):
    def get(self):
        return {'Hello': 'World!'}, 200


class AlbumBaseView(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('offset', type=int, location='args', required=False, default=1)
        self.parser.add_argument('limit', type=int, location='args', required=False, default=10)
        self.parser.add_argument('classification_id', location='args', required=False, type=int, default=0)
        self.parser.add_argument('name', type=str, location='json', default='')
        self.parser.add_argument('artist', type=str, location='json', default='')
        self.parser.add_argument('is_hot', type=bool, location='json')
        self.parser.add_argument('classification', type=int, location='json', action='append')

        classification_fields = {
            'id': fields.Integer(attribute='id'),
            'name': fields.String(attribute='name')
        }
        self.album_fields = {
            'id': fields.Integer(attribute='id'),
            'name': fields.String(attribute='name'),
            'artist': fields.String(attribute='artist'),
            'is_hot': fields.Boolean(attribute='is_hot'),
            'classification': fields.List(fields.Nested(classification_fields)),
        }
        self.resource_fields = {
            'error_code': fields.Integer(attribute='error_code')
        }


class AlbumListView(AlbumBaseView):
    def get(self):
        self.parser.remove_argument('name')
        self.parser.remove_argument('artist')
        self.parser.remove_argument('is_hot')
        self.parser.remove_argument('classification')
        self.resource_fields['data'] = fields.List(fields.Nested(self.album_fields))
        args = self.parser.parse_args()
        offset = args.get('offset')
        limit = args.get('limit')
        cl_id = args.get('classification_id')
        album_list = (Album.select()
                      .join(AlbumClassificationThrough)
                      .join(Classification)
                      .where(Classification.id == cl_id)
                      .paginate(offset, limit)) if  cl_id else (Album.select().paginate(offset, limit))
        data = [model_to_dict(album, backrefs=True, manytomany=True) for album in album_list]
        resp = {
            'error_code': 0,
            'data': data
        }
        return make_response(json.dumps(marshal(resp, self.resource_fields)), 200)

    def post(self):
        self.resource_fields['data'] = fields.Nested(self.album_fields)
        args = self.parser.parse_args()
        name = args.get('name', '')
        artist = args.get('artist', '')
        is_hot = args.get('is_hot', 0)
        classification = args.get('classification', [])

        cl_obj_list = Classification.select().where(Classification.id << classification)
        album = Album(
            name=name,
            artist=artist,
            is_hot=is_hot
        )
        album.save()

        cl_json_list = []
        if cl_obj_list.exists():
            for item in cl_obj_list:
                album.classification.add(item)
                cl_json_list.append(model_to_dict(item))
            album.save()
        album = model_to_dict(album)
        album['classification'] = cl_json_list
        resp = {
            'error_code': 0,
            'data': album
        }

        return make_response(json.dumps(marshal(resp, self.resource_fields)), 200)


class AlbumView(AlbumBaseView):
    def __init__(self):
        super(AlbumView, self).__init__()
        self.resource_fields['data'] = fields.Nested(self.album_fields, default={})

    def get(self, album_id):
        resp = {}
        album = Album.select().where(Album.id == album_id).first()
        if album:
            cl_obj_list = album.classification
            cl_json_list = []
            if cl_obj_list.exists():
                for item in cl_obj_list:
                    cl_json_list.append(model_to_dict(item))
            album = model_to_dict(album)
            album['classification'] = cl_json_list
            resp = {
                'error_code': 0,
                'data': album
            }

        return make_response(json.dumps(marshal(resp, self.resource_fields)), 200)

    def put(self, album_id):
        album = Album.select().where(Album.id == album_id).first()
        if album:
            status_code = 200
            args = self.parser.parse_args()
            classification = args.get('classification', [])
            cl_json_list = []

            """ Return album data without update if error classification data"""
            if type(classification) == type([]) and len(classification) != 0:
                cl_obj_list = Classification.select().where(Classification.id << classification)
                for item in cl_obj_list:
                    if item in album.classification:
                        continue
                    album.classification.add(item)
                    album.save()

            for item in album.classification:
                cl_json_list.append(model_to_dict(item))
            album = model_to_dict(album)
            album['classification'] = cl_json_list
            resp = {
                'error_code': 0,
                'data': album
            }

        else:
            status_code = 400
            self.resource_fields['message'] = fields.String(attribute='message')
            resp = {
                'error_code': 40021,
                'message': 'Album dose not exist.'
            }
        return make_response(json.dumps(marshal(resp, self.resource_fields)), status_code)


class ClassificationListView(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help="Name cannot be blank.")
        self.parser.add_argument('parent', type=int)

        self.classification_fields = {
            'id': fields.Integer(attribute='id'),
            'name': fields.String(attribute='name'),
            'parent': fields.Integer(attribute='parent')
        }

    def get(self):
        resource_fields = {
            'error_code': fields.Integer(attribute='error_code'),
            'data': fields.List(fields.Nested(self.classification_fields))
        }
        cl_list = Classification.select()
        data = [model_to_dict(cl) for cl in cl_list]
        resp = {
            'error_code': 0,
            'data': data
        }
        return make_response(json.dumps(marshal(resp, resource_fields)), 200)

    def post(self):
        resource_fields = {
            'error_code': fields.Integer(attribute='error_code'),
            'message': fields.String(attribute='message'),
            'data': fields.Nested(self.classification_fields)
        }
        args = self.parser.parse_args()
        name = args.get('name')
        parent_id = args.get('parent', None)
        if not (parent_id and Classification.select().where(Classification.id == parent_id).exists()):
            self.classification_fields.pop('parent')
        try:
            cl = Classification.create(
                name=name,
                parent=parent_id
            )
            status_code = 201
            resp = {
                'error_code': 0,
                'data': model_to_dict(cl)
            }
            resource_fields.pop('message')
        except IntegrityError:
            resp = {
                'error_code': 40020,
                'message': 'Duplicate name.'
            }
            resource_fields.pop('data')
            status_code = 400

        return make_response(json.dumps(marshal(resp, resource_fields)), status_code)

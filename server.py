from flask import Flask
from flask_restful import Resource, Api, reqparse, request

from key_value_storage import KeyValueStorage

app = Flask(__name__)
api = Api(app)

storage = KeyValueStorage()

parser_get = reqparse.RequestParser()
parser_get.add_argument('time', type=int)
parser_get.add_argument('time1', type=int)
parser_get.add_argument('time2', type=int)

parser_put = reqparse.RequestParser()
parser_put.add_argument('value', type=str, required=True, help="need value to put")

parser_del = reqparse.RequestParser()
parser_del.add_argument('value', type=str)


class Storage(Resource):
    def put(self, key):
        args = parser_put.parse_args()
        value = args['value']
        return storage.put(key, value), 201

    def get(self, key):
        args = parser_get.parse_args()
        if len(request.form) < 2:
            time = args['time']
            return storage.get(key, time)
        else:
            time1, time2 = args['time1'], args['time2']
            if time1 is None or time2 is None:
                return "time1 and time2 need to be set", 400
            return storage.diff(key, time1, time2) or ("can't find target key", 204)

    def delete(self, key):
        args = parser_del.parse_args()
        value = args['value']
        return storage.delete(key, value), 204


api.add_resource(Storage, '/<string:key>')

if __name__ == '__main__':
    app.run()

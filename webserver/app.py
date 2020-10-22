from flask import Flask
from flask_restful import Resource, Api, fields, reqparse

app = Flask(__name__)
api = Api(app)

fields = {
    "message": fields.String,
    "timestamp": fields.DateTime,
    "planned_length": fields.Float,
}

current_class = {
    "id": 0,
    "message": "",
    "timestamp": None,
    "planned_length": 0.,
}

parser = reqparse.RequestParser()
parser.add_argument("message", location='json')
parser.add_argument("timestamp", location='json')
parser.add_argument("planned_length", location='json')


class Updates(Resource):
    def get(self):
        return current_class

    # @marshal_with(fields)
    def post(self):
        args = parser.parse_args()
        current_class["message"] = args["message"]
        current_class["timestamp"] = args["timestamp"]
        current_class["planned_length"] = args["planned_length"]
        current_class["id"] += 1
        return 201


api.add_resource(Updates, '/updates')

if __name__ == '__main__':
    app.run(debug=False)

from flask import Flask
from flask_restful import Resource, Api, fields, reqparse
import datetime

app = Flask(__name__)
api = Api(app)

fields = {
    "message": fields.String,
    "timestamp": fields.DateTime,
    "planned_length": fields.Float,
}

current_class = {
    "id": 0,
    "message": "NO CLASS",
    "timestamp": None,
    "planned_length": 0.,
    "status": 0,
    "in_free_time": False,
}

parser = reqparse.RequestParser()
parser.add_argument("message", location='json')
parser.add_argument("timestamp", location='json')
parser.add_argument("planned_length", location='json')


class Updates(Resource):
    def get(self):
        if current_class["message"] == "freetime":
            current_class["in_free_time"] = True

        initial_time = datetime.datetime.strptime(current_class["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
        safe_time = datetime.timedelta(minutes=45) + initial_time
        clear_time = datetime.timedelta(hours=current_class["planned_length"]) + initial_time
        if datetime.datetime.now() > clear_time:
            current_class["status"] = 2             # Come on in!
        elif datetime.datetime.now() > safe_time:
            current_class["status"] = 1             # Knock before coming in!
        else:
            current_class["status"] = 0             # DON'T COME IN!

        return current_class

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

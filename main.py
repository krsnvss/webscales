from flask import Flask, jsonify, request
from flask_restful import abort, Api, reqparse, Resource
from configparser import ConfigParser
from datetime import datetime
from serial import Serial

app = Flask(__name__)
api = Api(app)
config = ConfigParser()
config.read('scales.ini')
scales_name = config['scales']['name']
scales_port = config['scales']['port']
scales_baudrate = config['scales']['baudrate']


def scribe(_str):
    with open("{}.txt".format(datetime.now().strftime("%d-%m-%Y")), "a") as log:
        log.write("{}\t{}".format(
            datetime.now().strftime("%H:%M:%S"),
            _str
        ))


class ScalesApi(Resource):

    def __init__(self):
        super(ScalesApi, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('scales', type=str)
        self.params = self.parser.parse_args()
        self.rs = Serial(
            port=scales_port,
            baudrate=scales_baudrate,
            bytesize=8,
            parity='N'
        )

    def get(self):
        with self.rs as rs:
            self.weight = rs.readline()
        scribe("Got scales value {}".format(str(self.weight)))
        self.errors = ''
        return jsonify({
            "scales": scales_name,
            "datetime": datetime.now(),
            "weight": self.weight,
            "errors": self.errors
        })


api.add_resource(ScalesApi, "/weight")

if __name__ == '__main__':
    app.run(debug=True)

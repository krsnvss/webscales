from flask import Flask, jsonify, request, render_template
from flask_restful import abort, Api, reqparse, Resource
from configparser import ConfigParser
from datetime import datetime
from serial import Serial
from random import randint

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


def get_value():
    serialport = Serial(
        port=scales_port,
        baudrate=scales_baudrate,
        bytesize=8,
        parity='N'
    )
    with serialport as rs:
        weight = rs.readline()
        scribe("Got scales value {}".format(str(weight)))
    return weight


class ScalesApi(Resource):

    def __init__(self):
        super(ScalesApi, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('scales', type=str)
        self.params = self.parser.parse_args()

    def get(self):
        self.errors = ''
        return jsonify({
            "scales": scales_name,
            "datetime": datetime.now(),
            "weight": self.weight,
            "errors": self.errors
        })


api.add_resource(ScalesApi, "/weight")


@app.route('/')
def index():
    value = randint(1000, 2000)
    return render_template('index.html', value=value)


if __name__ == '__main__':
    app.run(debug=True)

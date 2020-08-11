import os

import requests
import requests_cache
from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from pathlib import Path

# Setup functions to read from .env file
from utils import validate_latitude, validate_longitude, validate_units

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}" \
                       "&APPID={key}&units={units}"
WEATHERBIT_API_URL = "https://api.weatherbit.io/v2.0/alerts?lat={lat}&lon={lon}&key={key}"

app = Flask(__name__)
CORS(app)

requests_cache.install_cache(cache_name='openweathermap_cache', backend='sqlite', expire_after=600)


@app.route('/health')
def hello_world():
    return jsonify({"server status": "UP"})


@app.route('/alerts', methods=['GET'])
def alerts():
    errors = []
    check_empty_params(errors)
    if len(errors) > 0:
        return jsonify({"errors": errors})

    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    check_invalid_params(errors, latitude, longitude)

    if len(errors) > 0:
        return jsonify({"errors": errors})

    url = WEATHERBIT_API_URL.format(lat=latitude, lon=longitude, key=os.getenv("WB_API_KEY"))

    response_dict = requests.get(url).json()
    for alert in response_dict['alerts']:
        head, sep, _ = alert['description'].partition('.')
        alert['description'] = head + sep
    return jsonify(response_dict)


@app.route('/onecall', methods=['GET'])
def one_call():
    errors = []
    check_empty_params(errors)

    if len(errors) > 0:
        return jsonify({"errors": errors})

    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    units = request.args.get('units') if 'units' in request.args else 'default'

    check_invalid_params(errors, latitude, longitude)
    if not validate_units(units):
        errors.append("Invalid units")

    if len(errors) > 0:
        return jsonify({"errors": errors})

    url = OPEN_WEATHER_API_URL.format(lat=latitude, lon=longitude, units=units, key=os.getenv("OWM_API_KEY"))

    response_dict = requests.get(url).json()
    return jsonify(response_dict)


def check_empty_params(errors):
    if 'lat' not in request.args:
        errors.append("Missing latitude")
    if 'lon' not in request.args:
        errors.append("Missing longitude")


def check_invalid_params(errors, latitude, longitude):
    if not validate_latitude(latitude):
        errors.append("Invalid latitude")
    if not validate_longitude(longitude):
        errors.append("Invalid longitude")


if __name__ == '__main__':
    app.run(port=5000)

import os

import requests
import requests_cache
from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
from pathlib import Path

# Setup functions to read from .env file
from utils import validate_latitude, validate_longitude, validate_units

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}" \
                       "&APPID={key}&units={units}"

app = Flask(__name__)
requests_cache.install_cache(cache_name='openweathermap_cache', backend='sqlite', expire_after=600)


@app.route('/health')
def hello_world():
    return jsonify({"server status": "UP"})


@app.route('/onecall', methods=['GET'])
def one_call():
    errors = []
    if 'lat' not in request.args:
        errors.append("Missing latitude")
    if 'lon' not in request.args:
        errors.append("Missing longitude")

    if len(errors) > 0:
        return jsonify({"errors": errors})

    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    units = request.args.get('units') if 'units' in request.args else 'default'

    if not validate_latitude(latitude):
        errors.append("Invalid latitude")
    if not validate_longitude(longitude):
        errors.append("Invalid longitude")
    if not validate_units(units):
        errors.append("Invalid units")

    if len(errors) > 0:
        return jsonify({"errors": errors})

    url = OPEN_WEATHER_API_URL.format(lat=latitude, lon=longitude, units=units, key=os.getenv("API_KEY"))

    response_dict = requests.get(url).json()
    return jsonify(response_dict)


if __name__ == '__main__':
    app.run(port=5000)

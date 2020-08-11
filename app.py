import os

import requests
import requests_cache
from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
from pathlib import Path

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
requests_cache.install_cache(cache_name='openweathermap_cache', backend='sqlite', expire_after=600)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/weather', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=53.480720&lon=-2.240810&APPID={key}" \
              "&units=metric".format(key=os.getenv('API_KEY'))
        response_dict = requests.get(url).json()
        return jsonify(response_dict)
    return jsonify({"message": "Hello world!"})


if __name__ == '__main__':
    app.run(port=5000)

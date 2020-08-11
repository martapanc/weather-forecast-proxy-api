import requests
import requests_cache
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/weather', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=53.480720&lon=-2.240810&APPID={key}&units=metric"
        response_dict = requests.get(url).json()
        return jsonify(response_dict)
    return jsonify({"message": "Hello world!"})


if __name__ == '__main__':
    app.run(port=5000)

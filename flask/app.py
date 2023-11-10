from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
from weather import OpenWeatherMap

app = Flask(__name__)
CORS(app=app)
weather = OpenWeatherMap()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get_weather_data", methods=['GET'])
def get_weather_data():
    response = {}
    city = request.args.get('city')
    data = weather.get_weather(city)
    response = data
    response['city'] = city
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)

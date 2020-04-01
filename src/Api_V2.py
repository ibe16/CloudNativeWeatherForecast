from flask import Flask, jsonify
app = Flask(__name__)

from WeatherForecast import WeatherForecast
wf = WeatherForecast()


@app.route("/servicio/v2/prediccion/hours24", methods=['GET'])
def get_24hours_prediction():
    return jsonify(wf.make_forecast_from_api(24))


@app.route("/servicio/v2/prediccion/hours48", methods=['GET'])
def get_48hours_prediction():
    return jsonify(wf.make_forecast_from_api(48))


@app.route("/servicio/v2/prediccion/hours72", methods=['GET'])
def get_72hours_prediction():
    return jsonify(wf.make_forecast_from_api(72))


# if __name__ == '__main__':
#     app.run()
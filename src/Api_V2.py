# Versión 2 de la API
# Hace consultas a una API externa usando la clase WeatherForecast

from flask import Flask, jsonify
app = Flask(__name__)

from WeatherForecast import WeatherForecast
wf = WeatherForecast()


# Predicciones para dentro de 24 horas
@app.route("/servicio/v2/prediccion/hours24", methods=['GET'])
def get_24hours_prediction():
    return jsonify(wf.make_forecast_from_api(24))


# Predicciones para dentro de 48 horas
@app.route("/servicio/v2/prediccion/hours48", methods=['GET'])
def get_48hours_prediction():
    return jsonify(wf.make_forecast_from_api(48))


# Predicciones para dentro de 72 horas
@app.route("/servicio/v2/prediccion/hours72", methods=['GET'])
def get_72hours_prediction():
    return jsonify(wf.make_forecast_from_api(72))


# if __name__ == '__main__':
#     app.run()
# Versión 1 de la API
# Predice los datos con modelos ARIMA usando la clase WeatherForecast

from flask import Flask, jsonify
app = Flask(__name__)

from WeatherForecast import WeatherForecast
wf = WeatherForecast()
wf.create_model()
wf.save_model()

# Predicciones para dentro de 24 horas
@app.route("/servicio/v1/prediccion/hours24", methods=['GET'])
def get_24hours_prediction():
    return jsonify(wf.make_forecast_from_model(24))

# Predicciones para dentro de 48 horas
@app.route("/servicio/v1/prediccion/hours48", methods=['GET'])
def get_48hours_prediction():
    return jsonify(wf.make_forecast_from_model(48))

# Predicciones para dentro de 72 horas
@app.route("/servicio/v1/prediccion/hours72", methods=['GET'])
def get_72hours_prediction():
    return jsonify(wf.make_forecast_from_model(72))



# if __name__ == '__main__':
#     app.run()
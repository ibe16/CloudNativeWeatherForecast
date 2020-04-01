from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm

import pickle
import requests

from DataBase import load_from_database

import os
URL = os.environ['FORECAST_URL']

class WeatherForecast:
    """Clase para realizar predicciones sobre el tiempo"""

    def __init__(self):
        self.data = load_from_database()
        # path1="/tmp/workflow/humidity.csv"
        # path2="/tmp/workflow/temperature.csv"
        # data_humidity = pd.read_csv(path1, header=0)
        # data_temperature = pd.read_csv(path2, header=0)
        
        # data_humidity = data_humidity[["datetime", "San Francisco"]]
        # data_humidity= data_humidity.rename(columns={'San Francisco': 'SFHumidity'})

        # data_temperature = data_temperature[["datetime", "San Francisco"]]
        # data_temperature = data_temperature.rename(columns={'San Francisco': 'SFTemperature'})

        # data = pd.merge(data_temperature, data_humidity, on='datetime')
        # data = data.dropna()
        # data.reset_index(inplace=True)

        self.data = self.data.head(1000)

    def create_model(self):
        self.model_humidity = pm.auto_arima(self.data['SFHumidity'], start_p=1, start_q=1,
        test='adf', 
        max_p=3, max_q=3,
        m=1,
        d=None,
        seasonal=False,
        start_P=0, 
        D=0,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True)

        self.model_temperature = pm.auto_arima(self.data['SFTemperature'], start_p=1, start_q=1,
        test='adf', 
        max_p=3, max_q=3,
        m=1,
        d=None,
        seasonal=False,
        start_P=0, 
        D=0,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True)

    def save_model(self):
        with open("model_humidity.pickle", 'wb') as f:
            pickle.dump(self.model_humidity, f, pickle.HIGHEST_PROTOCOL)

        with open("model_temperature.pickle", 'wb') as f:
            pickle.dump(self.model_temperature, f, pickle.HIGHEST_PROTOCOL)

    def load_model(self):
        with open("./models/model_humidity.pickle", 'rb') as f:
            self.model_humidity = pickle.load(f)

        with open("./models/model_temperature.pickle", 'rb') as f:
            self.model_temperature = pickle.load(f)

    def make_forecast_from_model(self, periods):
        fc_temp, confint = self.model_temperature.predict(n_periods=periods, return_conf_int=True)
        fc_hum, confint = self.model_humidity.predict(n_periods=periods, return_conf_int=True)

        result = {"hours" : periods,
                  "temperature" : fc_temp[periods-1], 
                  "humidity" : fc_hum[periods-1]}

        print(result)
        return result

    def make_forecast_from_api(self, periods):
        response = requests.get(url=URL)
        data = response.json()
 
        if int(periods) == 24:
            day=1
        elif int(periods) == 48:
            day=2
        else:
            day=3
        
        forecast_temp = data['forecasts'][day]['day']['temp']
        forecast_hum = data['forecasts'][day]['day']['rh']

        result = {"hours" : periods,
                  "temperature" : forecast_temp, 
                  "humidity" : forecast_hum}

        print(result)
        return result

if __name__ == "__main__":
    wf = WeatherForecast()
    #wf.create_model()
    # wf.save_model()
    wf.load_model()
    wf.make_forecast_from_model(24)
    wf.make_forecast_from_model(48)
    wf.make_forecast_from_model(72)
    wf.make_forescast_from_api(24)
    wf.make_forescast_from_api(48)
    wf.make_forescast_from_api(72)

    
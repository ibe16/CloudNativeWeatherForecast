from pymongo import MongoClient
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
import json

import os
URI = os.environ['MONGO_URI']

client = MongoClient(URI)
db = client["SanFrancisco"]
weather_data = db["weather_data"]

def save_on_database(path1, path2):
    data_humidity = pd.read_csv(path1, header=0)
    data_temperature = pd.read_csv(path2, header=0)
    
    data_humidity = data_humidity[["datetime", "San Francisco"]]
    data_humidity= data_humidity.rename(columns={'San Francisco': 'SFHumidity'})

    data_temperature = data_temperature[["datetime", "San Francisco"]]
    data_temperature = data_temperature.rename(columns={'San Francisco': 'SFTemperature'})

    data = pd.merge(data_temperature, data_humidity, on='datetime')
    data = data.dropna()
    data.reset_index(inplace=True)

    data_dict = data.to_dict("records")
    weather_data.insert_one({"index":"SF","data":data_dict})

    return None

def load_from_database():
    data_from_db = weather_data.find_one({"index":"SF"})
    df = pd.DataFrame(data_from_db["data"])
    df.set_index("index",inplace=True)
    print(df)

    return df

if __name__ == "__main__":
    save_on_database("/tmp/workflow/humidity.csv", "/tmp/workflow/temperature.csv")
    load_from_database()

from pymongo import MongoClient
import pandas as pd
import json

import os
URI = os.environ['MONGO_URI']

# Conexión con la base de datos
client = MongoClient(URI)
db = client["SanFrancisco"] # Nombre de la base de datos
weather_data = db["weather_data"] # Nombre de la colección

def save_on_database(path1, path2):
    """ Fucnión que lee dos ficheros de temperatura y humedas, los 
        transforma a dataframe y los almacena en la base de datos"""

    # Lee los ficheros CSV
    data_humidity = pd.read_csv(path1, header=0)
    data_temperature = pd.read_csv(path2, header=0)
    
    # Selecciona las columnas necesarias de los datos de humedad
    data_humidity = data_humidity[["datetime", "San Francisco"]]
    data_humidity= data_humidity.rename(columns={'San Francisco': 'SFHumidity'})

    # Selecciona las columnas necesarias de los datos de temperatura
    data_temperature = data_temperature[["datetime", "San Francisco"]]
    data_temperature = data_temperature.rename(columns={'San Francisco': 'SFTemperature'})

    # Una los datos por la columna datetime
    data = pd.merge(data_temperature, data_humidity, on='datetime')
    data = data.dropna()
    data.reset_index(inplace=True)

    # Guarda los datos en la BD
    data_dict = data.to_dict("records")
    weather_data.insert_one({"index":"SF","data":data_dict})

    return None

def load_from_database():
    """ Carga el dataframe de la base de datos y lo devuelve """

    data_from_db = weather_data.find_one({"index":"SF"})
    df = pd.DataFrame(data_from_db["data"])
    df.set_index("index",inplace=True)
    print(df)

    return df

# if __name__ == "__main__":
#     save_on_database("/tmp/workflow/humidity.csv", "/tmp/workflow/temperature.csv")
#     load_from_database()

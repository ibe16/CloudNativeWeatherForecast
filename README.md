# CloudNativeWeatherForecast
Repositorio para la práctica 2 de la asignatura Cloud Computing: Servicios y Aplicaciones

API RESTful para la predicción de la temperatura y la humedad de la ciudad de San Francisco usando modelos ARIMA y la API de [The Weather Company.][api_the_weather]

Para el despliegue se ha usado un flujo de trabajo de Airflow.

## Requisitos del sistema
1. Tener instalado Python 3.6
2. Instalar [Airflow][airflow].
3. Cumplir con las dependencias que se indican en el archivo [requirements.txt.][requirements]. Para instalarlas se puede ejecutar la siguiente orden:
    ```shell
    pip install -r requirements.txt
    ```
4. Declarar las siguientes variables de entorno en la terminal dónde se ejecute el **scheduler** de Airflow:
    * MONGO_URI → URI de la conexión con la base de datos de MongoDB desde fuera del contenedor que la contiene
    * MONGO_URI_DOCKER → URI de la conexión con la base de datos dentro de la red Docker.
    * FORECAST_URL → URL que contiene la dirección dónde se realizarán las peticiones para realizar la previsión de la temperatura y la humedad. Se explica cómo conseguirla en la sección 3.2.
5. Tener instalado [Docker][docker] y [docker-compose][docker-compose].

[api_the_weather]: https://weather.com/swagger-docs/call-for-code
[airflow]: https://airflow.apache.org/docs/stable/installation.html
[requirements]: https://github.com/ibe16/CloudNativeWeatherForecast/blob/master/requirements.txt
[docker]: https://docs.docker.com/install/
[docker-compose]: https://docs.docker.com/compose/install/

from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Importamos el archivo donde se encuentra la función que accede a la base de datos
import sys
sys.path.append("/home/irene/MEGA/CC2/Practica2/src")
from DataBase import save_on_database


default_args = {'owner': 'airflow',
'depends_on_past': False,
'start_date': days_ago(2),   #como no se ha ejecutado se pone primero en la cola
'email': ['airflow@example.com'],
'email_on_failure': False,
'email_on_retry': False,
'retries': 1,
'retry_delay': timedelta(minutes=5)
}

#Inicialización del grafo DAG de tareas para el flujo de trabajo
dag = DAG('practica2_dag',
default_args=default_args,
description='Practica 2',
schedule_interval='@once', # Se ejecuta solo una vez
catchup=False # No tiene encuenta las ejecuciones atrasadas
)

# Crear la carpeta donde se van a guardar los archivos
PrepararEntorno = BashOperator(
    task_id='PrepararEntorno',
    depends_on_past=False,
    bash_command='mkdir -p /tmp/workflow/',
    dag=dag)

# Descarga los datos sobre la humedad de San Francisco en formato zip
CapturarDatosHumedad = BashOperator(
    task_id='CapturarDatosHumedad',
    depends_on_past=True,
    bash_command='wget --output-document /tmp/workflow/humidity.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',
    dag=dag)

# Descarga los datos sobre la temperatura de San Francisco en formato zip
CapturarDatosTemperatura = BashOperator(
    task_id='CapturarDatosTemperatura',
    depends_on_past=True,
    bash_command='wget --output-document /tmp/workflow/temperature.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',
    dag=dag)

# Descarga el repositorio de Git donde se encuentra el código en formato zip
Descargar_Repo = BashOperator(
    task_id='Descargar_Repo',
    depends_on_past=True,
    bash_command='wget --output-document /tmp/workflow/master.zip https://github.com/ibe16/CloudNativeWeatherForecast/archive/master.zip',
    dag=dag
)

# Descomprime todos los ficheros .zip en el directorio de trabajo
DescomprimirDatos = BashOperator(
    task_id='DescomprimirDatos',
    depends_on_past=True,
    bash_command='unzip -o /tmp/workflow/\*.zip -d /tmp/workflow/',
    dag=dag
)


# Levanta el contenedor con la BD de MongoDB
Levantar_DB = BashOperator(
    task_id='Levantar_DB', 
    depends_on_past=True,
    bash_command='docker-compose -f /tmp/workflow/CloudNativeWeatherForecast-master/docker-compose.yml up -d mongodb',
    dag=dag
)

# Función de Python que almacena un dataframe de Pandas en la BD
Guardar_Temp_Hum_DB = PythonOperator(
    task_id='Guardar_Temp_Hum_BD',
    python_callable=save_on_database,
    op_kwargs={'path1': "/tmp/workflow/humidity.csv",
                'path2': "/tmp/workflow/temperature.csv"}, 
    dag=dag
)

# Ejecuta los test unitarios
Unit_Tests = BashOperator(
    task_id='Unit_Tests',
    depends_on_past=True,
    bash_command='python3 -m unittest discover /tmp/workflow/CloudNativeWeatherForecast-master/tests',
    dag=dag
)

# Levanta los contenedores que tienen las APIs
Despliegue_En_Contenedores = BashOperator(
    task_id='Despliegue_En_Contenedores', 
    depends_on_past=True,
    bash_command='docker-compose -f /tmp/workflow/CloudNativeWeatherForecast-master/docker-compose.yml up -d',
    dag=dag
)


# Grafo de las tareas
PrepararEntorno >> [CapturarDatosHumedad, CapturarDatosTemperatura, Descargar_Repo]
[CapturarDatosHumedad, CapturarDatosTemperatura, Descargar_Repo] >> DescomprimirDatos >> Levantar_DB
Levantar_DB >> Guardar_Temp_Hum_DB >> Unit_Tests >> Despliegue_En_Contenedores

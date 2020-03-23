from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests


# Inluir biliotecas PIP


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
schedule_interval=timedelta(days=1),
)

PrepararEntorno = BashOperator(
    task_id='PrepararEntorno',
    depends_on_past=False,
    bash_command='mkdir -p /tmp/workflow/',
    dag=dag)

CapturarDatosHumedad = BashOperator(
    task_id='CapturarDatosHumedad',
    depends_on_past=True,
    bash_command='wget --output-document /tmp/workflow/humidity.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',
    dag=dag)

CapturarDatosTemperatura = BashOperator(
    task_id='CapturarDatosTemperatura',
    depends_on_past=True,
    bash_command='wget --output-document /tmp/workflow/temperature.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',
    dag=dag)

DescomprimirDatos = BashOperator(
    task_id='DescomprimirDatosHumedad',
    depends_on_past=True,
    bash_command='unzip /tmp/workflow/humidity.csv.zip /tmp/workflow/temperature.csv.zip -d /tmp/workflow/',
    dag=dag
)

# DescomprimirDatosHumedad = BashOperator(
#     task_id='DescomprimirDatosHumedad',
#     depends_on_past=True,
#     bash_command='unzip /tmp/workflow/humidity.csv.zip -d /tmp/workflow/',
#     dag=dag
# )

# DescomprimirDatosTemperatura = BashOperator(
#     task_id='DescomprimirDatosTemperatura',
#     depends_on_past=True,
#     bash_command='unzip /tmp/workflow/temperature.csv.zip -d /tmp/workflow/',
#     dag=dag
# )


PrepararEntorno >> [CapturarDatosHumedad, CapturarDatosTemperatura]
[CapturarDatosHumedad, CapturarDatosTemperatura] >> DescomprimirDatos
# CapturarDatosHumedad >> DescomprimirDatosHumedad
# CapturarDatosTemperatura >> DescomprimirDatosTemperatura
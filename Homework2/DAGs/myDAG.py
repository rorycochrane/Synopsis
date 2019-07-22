import pandas as pd
from datetime import datetime, timedelta

import requests
import alpha_vantage

from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='YADS9AQEC5BOFNJK',output_format='pandas')
# Get json object with the intraday data and another with  the call's metadata
def Get_stocks():
  data, meta_data = ts.get_intraday('TSLA')
  data.to_csv('stock_data.csv')

#Airflow
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(3),
    'depends_on_past': False,
    'email': ['rory.m.cochrane@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
  'Homework2',
  default_args=default_args,
  description='DAG for Homework 2',
  schedule_interval=timedelta(days=1)
)

t1 = PythonOperator(
  task_id='get_stock_info',
  python_callable=get_stocks,
  provide_context=True,
  dag=dag
)
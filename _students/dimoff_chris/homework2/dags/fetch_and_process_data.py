from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 20),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('my_first_dag', default_args=default_args, schedule_interval=timedelta(days=1))


def fetch_data(**kwargs):
    response = requests.get('http://www.reddit.com/r/weather.json', headers = {'User-agent': 'My Dag Bot'}).json()


    return response


def process(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids='fetch_data')
    data = []
    for i in range(10):
        chunk = raw_data['data']['children'][i]['data']


        title = chunk['title']
        thumbnail = chunk['thumbnail']
        permalink = chunk['permalink']
        data.append({"title": chunk['title'], "thumbnail": chunk['thumbnail'], "permalink": permalink})

    df = pd.DataFrame(data)
    df.to_csv('./output/output.csv')


fetch_data = PythonOperator(
    task_id='fetch_data',
    dag=dag,
    python_callable=fetch_data,
    provide_context = True
)

process = PythonOperator(
    task_id='process',
    dag=dag,
    python_callable=process,
    provide_context = True
)

process.set_upstream(fetch_data)


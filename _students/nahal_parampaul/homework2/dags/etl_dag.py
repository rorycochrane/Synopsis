import json
import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 28),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Instantiate a DAG
dag = DAG('hw2_dag', default_args=default_args, schedule_interval=timedelta(days=1))

# ==== EXTRACT ================= # 
def get_frontpage_videos():
    """Get reddit.com/r/videos frontpage data and save to disk."""

    url = 'https://www.reddit.com/r/videos.json'
    export_filename = f"data/raw/videos-frontpage-raw_{str(datetime.now().date())}.json"
    
    # Get reddit videos front page data
    r = requests.get(url, headers={'User-Agent': 'dag-nab-it'})
    
    # Save the json response to disk
    with open(export_filename, 'w') as json_file:
        json.dump(r.json(), json_file)
            
t1 = PythonOperator(
    task_id='get_frontpage_videos',
    python_callable=get_frontpage_videos,
    retries=3,
    dag=dag)

# ==== TRANSFORM / LOAD ================= # 
def process_video_titles_to_csv():
    """Process json data to extract title and url of videos.
    
    Then save results as CSV
    """
    
    import_filename = f"data/raw/videos-frontpage-raw_{str(datetime.now().date())}.json"
    export_filename = f"data/processed/videos-frontpage_{str(datetime.now().date())}.txt"
    
    # Load json response
    with open(import_filename) as json_file:
        data = json.load(json_file)
    
    # Process and save CSV file
    with open(export_filename, 'w') as file:
        file.write(f'title,url\n')

        for video in data['data']['children']:
            
            vid_title = video['data']['title'].replace(","," ")
            vid_url = video['data']['url'].partition("&")[0]

            file.write(f"{vid_title},{vid_url}\n")
            
t2 = PythonOperator(
    task_id='process_video_titles_to_csv',
    python_callable=process_video_titles_to_csv,
    retries=3,
    dag=dag)

# t2 depends on t1 
t2.set_upstream(t1)
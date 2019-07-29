# 7gate-hw2-data-pipeline


## Running Airflow
1. Type `docker-compose up`
2. Visit: http://localhost:8080/admin/

## High Level
1. Get all reddit.com/r/videos front page entries
	- Save results in a json file
2. Process results to extract video title and url
3. Store in a daily CSV w/ timestamp

### Helpful Links
- https://docs.python.org/2/library/sqlite3.html
- https://airflow.apache.org/tutorial.html
- http://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/

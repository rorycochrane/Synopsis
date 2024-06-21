# HomeWork 2 -- Create Dag in Airflow
### Overview
This homework was created for 7gates Machine Learning bootcamp. It is a simple pipeline that extracts data from reddit.com/r/weather, parses it, and stores key values into a csv.

## Running The Repo
- Git clone it
- `docker-compose up`
- Dag should run automatically but you may have to turn it on and trigger it.

## Source Data
www.reddit.com/r/weather

## Pipleline Logic
The pipeline consists of two tasks: fetch task and parse/process task. The fetch task takes the data and passes it to the second task via context.
The process task then parses the title, thumbnail image url, and post url and then saves it into .csv.

## Output
output.csv file in ./output
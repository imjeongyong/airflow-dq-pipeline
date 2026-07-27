from datetime import datetime
from airflow.sdk import dag, task

@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["sample"],
)
def sample_pipeline():

    @task
    def extract():
        print("데이터 수집했다 치자")
        return {"rows": 100}

    @task
    def validate(data):
        print(f"검증: {data['rows']}건 받음, 통화했다 치자")
        return data

    @task
    def load(data):
        print(f"적재: {data['rows']}건 적재했다 치자")

    load(validate(extract()))

sample_pipeline()
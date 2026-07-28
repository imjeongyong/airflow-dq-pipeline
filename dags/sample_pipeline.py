from datetime import datetime, timedelta
from airflow.sdk import dag, task

# 모든 태스크에 공통 적용될 기본 설정
default_args= {
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["sample"],
)
def sample_pipeline():

    @task
    def extract():
        print("데이터 수집했다 치자")
        return 100

    # @task
    # def extract():
    #     import random
    #     print("데이터 수집 시도")
    #     if random.random() < 0.7:
    #         raise ValueError("API 응답 없음 (일시 장애 시뮬레이션)")
    #     return 100

    @task
    def load(collected):
        print(f"적재: {collected}건 적재했다 치자")
        return 100

    @task
    def reconcile(collected, loaded):
        print(f"정합성 점검: 수집 {collected} vs 적재 {loaded}")
        if collected != loaded:
            raise ValueError(f"불일치 발생! 수집 {collected} != 적재 {loaded}")
        print("정합성 OK!")

    # 의존성: extract -> load -> reconcile
    collected = extract()
    loaded = load(collected)
    reconcile(collected, loaded)

sample_pipeline()
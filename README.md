# DE Pipeline — 데이터 품질 검증 중심 ETL 파이프라인

공공 API 데이터를 수집하여 DQ 검증·reconciliation을 거쳐
레이어드 DW(Raw/Core/Mart)로 적재하는 Airflow 기반 파이프라인.

## 기술 스택
- Orchestration: Apache Airflow 3.x
- Database: PostgreSQL
- Infra: Docker / Docker Compose

## 실행 방법
```bash
docker compose up airflow-init   # 최초 1회
docker compose up -d
```
Airflow UI: http://localhost:8080 (airflow / airflow)

## 진행 상태
- [x] Airflow 로컬 환경 구축
- [ ] 샘플 DAG
- [ ] 공공 API 수집
- [ ] DQ 검증 + reconciliation
- [ ] 레이어드 DW (Raw/Core/Mart)
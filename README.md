# airflow-dq-pipeline

데이터 품질 검증(DQ)과 정합성 대사(reconciliation)를 중심에 둔 Airflow 기반 데이터 파이프라인.

> **상태**: 🚧 개발 중 — 로컬 Airflow 환경 구축 및 파이프라인 뼈대 완료. 도메인 로직(공공 기상 데이터 분석) 구현 예정.

---

## 프로젝트 개요

공공 API 데이터를 수집하여 **품질 검증(DQ)** 과 **수집–적재 건수 정합성 대사(reconciliation)** 를 거쳐, 레이어드 데이터 웨어하우스(Raw / Core / Mart)로 적재하는 Airflow 파이프라인.

**설계 철학**: 공공기관 데이터 연계 실무(다기관 수집·정합성 검증·재처리)에서 다뤄온 데이터 품질·정합성 관리를 업계 표준 스택(Airflow / dbt / Docker)으로 재현하는 것을 목표로 한다.

### 두 개의 핵심 축 (signature)

1. **DQ + reconciliation** — 스키마 검증, 수집 건수 vs 적재 건수 대사로 적재 누락·중복을 사전 탐지
2. **레이어드 DW** — Raw(원천 보존) → Core(정제·표준화) → Mart(분석용 집계)의 계층 구조 (Medallion)

---

## 기술 스택

| 구분 | 스택 |
|---|---|
| Orchestration | Apache Airflow 3.x |
| Database | PostgreSQL |
| Infra | Docker / Docker Compose |
| Transform (예정) | dbt |
| Processing (예정) | Python (pandas), PySpark |
| Cloud (예정) | AWS (S3 / RDS) |
| BI (예정) | Metabase / Looker Studio |

---

## 실행 방법

```bash
# 최초 1회: DB 초기화 + 관리자 계정 생성
docker compose up airflow-init

# 전체 스택 구동
docker compose up -d

# 상태 확인
docker compose ps
```

- Airflow UI: http://localhost:8080 (기본 계정 `airflow` / `airflow`)
- 종료: `docker compose down`

### 요구 사항
- Docker Desktop (WSL2 백엔드)
- Docker에 4GB 이상 메모리 할당 권장 (Airflow 컴포넌트 다수 구동)

---

## 프로젝트 구조

```
airflow-dq-pipeline/
├── docker-compose.yaml       # Airflow 3.x 스택 정의
├── .env                      # 환경변수 (git 제외, .env.example 참고)
├── dags/                     # Airflow DAG 정의
│   └── sample_pipeline.py    # 샘플 DAG (extract → load → reconcile)
├── include/                  # DAG 보조 코드 (예정)
│   ├── ingest/               #   데이터 수집 로직
│   ├── dq/                   #   DQ 검증 · reconciliation
│   └── sql/                  #   Raw/Core/Mart SQL
├── plugins/                  # 커스텀 플러그인
└── logs/                     # 실행 로그 (git 제외)
```

---

## 현재 구현 상태

- [x] Docker 기반 Airflow 3.x 로컬 환경 구축 (`docker compose up` 단일 명령 재현)
- [x] 샘플 DAG: `extract → load → reconcile` (retry, XCom 기반 건수 대조 포함)
- [ ] 공공 API 데이터 수집 (기상청 예보 / 실황)
- [ ] DQ 검증 룰 (스키마 · 건수 · 결측 · 중복)
- [ ] reconciliation (API 응답 건수 = Raw 적재 건수 대사)
- [ ] 레이어드 DW (Raw / Core / Mart)
- [ ] dbt 모델 + dbt tests
- [ ] BI 대시보드
- [ ] AWS(S3/RDS) 통합
- [ ] PySpark 처리 파트

---

## 로드맵 (도메인 적용 예정)

현재 파이프라인 뼈대 위에, **공공 기상 데이터 기반 분석 도메인**을 얹을 예정:

> 기상 예보와 실제 관측 데이터를 수집·대조하여, 골프장 악천후 시 예약취소 기준의 합리성을 데이터로 검증·제안하는 파이프라인.

- **수집원 다양성**: 공공 API(기상청 예보·실황) + 웹 스크래핑 + 반정형(기상특보 통보문)
- **reconciliation**: API 응답 건수와 Raw 적재 건수를 대사하여 수집 무결성 보장
- **도메인 분석**: 예보 시점별 정확도를 검증해 "예보 신뢰도가 실용 수준에 도달하는 시점"을 도출

*(도메인 로직 구현 시 본 README를 상세화 예정)*

---

## 학습 기록

Docker · Airflow를 처음부터 학습하며 구축한 과정과 트러블슈팅을 별도 문서로 정리 (환경 셋업, DAG 작성, 디버깅 방법론 등).
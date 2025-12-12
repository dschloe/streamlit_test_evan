from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
from pandas_gbq import to_gbq
from dotenv import load_dotenv
import os

# 1. 환경 변수 로드 및 검증
loaded = load_dotenv()  # .env 파일 읽기
print(f".env 파일 로드 성공 여부: {loaded}")

KEY_PATH = os.getenv("GCP_KEY_PATH")
print(KEY_PATH)

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

PROJECT_ID = credentials.project_id
DATASET_ID = "demo"                     # 대상 데이터셋
TABLE_NAME = "orders"                   # 생성할 테이블 이름
FILE_PATH = "data/orders.xlsx"          # 로컬 엑셀 파일 경로
destination = f"{DATASET_ID}.{TABLE_NAME}"

df = pd.read_excel(FILE_PATH)

# 2. BigQuery 업로드 (demo 데이터셋의 orders 테이블)
to_gbq(
    df, 
    destination_table=destination,
    project_id=PROJECT_ID,
    credentials=credentials,
    if_exists="replace"  # 'replace': 덮어쓰기, 'append': 추가하기
)

print("업로드 완료")
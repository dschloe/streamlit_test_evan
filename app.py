import streamlit as st
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import bigquery

# 1. 환경 변수 로드
load_dotenv()

# .env 파일에서 변수 가져오기 (없으면 None이 들어가며 이후 단계에서 에러 발생)
KEY_PATH = os.getenv("GCP_KEY_PATH")

# 페이지 설정
st.set_page_config(page_title="BigQuery Dashboard", layout="wide")
st.title("BigQuery Orders Dashboard (Raw Mode)")

# 2. 데이터 로드 함수 (캐싱 적용)
@st.cache_data(ttl=600)
def load_data():
    # 인증 객체 생성 (파일 경로가 틀리면 여기서 FileNotFoundError 발생)
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    
    # 클라이언트 생성
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 쿼리 작성 및 실행
    query = """
        SELECT * FROM `demo.orders`
        LIMIT 1000
    """
    
    # 결과를 DataFrame으로 변환 (쿼리 오류 시 여기서 GoogleCloudError 발생)
    return client.query(query).to_dataframe()

# 3. 데이터 불러오기 실행
# 에러 처리가 없으므로 문제 발생 시 앱 실행이 중단되고 에러 메시지가 뜹니다.
df = load_data()

# 4. 결과 시각화
st.success("데이터 로드 성공!")

col1, col2 = st.columns(2)
with col1:
    st.metric("조회된 데이터 수", f"{len(df)} 건")
with col2:
    st.metric("컬럼 수", f"{len(df.columns)} 개")

st.subheader("데이터 미리보기")
st.dataframe(df, width="stretch")
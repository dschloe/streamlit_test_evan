import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# 페이지 설정
st.set_page_config(page_title="BigQuery Dashboard", layout="wide")
st.title("BigQuery Dashboard (Secrets Mode)")

# 1. 데이터 로드 함수 (캐싱 적용)
@st.cache_data(ttl=600)
def load_data():
    # [변경 핵심] st.secrets에서 정보 가져오기 (dict 형태)
    # secrets.toml 파일의 [gcp_service_account] 섹션을 읽어옵니다.
    key_info = st.secrets["gcp_service_account"]
    
    # [변경 핵심] 파일 경로(_file)가 아니라 정보(_info)로 인증 객체 생성
    creds = service_account.Credentials.from_service_account_info(key_info)
    
    # 클라이언트 생성 (project_id도 secrets에서 가져옴)
    client = bigquery.Client(credentials=creds, project=key_info["project_id"])

    # 쿼리 작성
    query = """
        SELECT * FROM `demo.orders`
        LIMIT 1000
    """
    
    # 실행 및 데이터프레임 변환
    return client.query(query).to_dataframe()

# 2. 데이터 불러오기 (try-except 없음)
df = load_data()

# 3. 결과 시각화
st.success("Secrets를 통한 데이터 로드 성공!")

col1, col2 = st.columns(2)
with col1:
    st.metric("조회된 데이터 수", f"{len(df)} 건")
with col2:
    st.metric("컬럼 수", f"{len(df.columns)} 개")

st.subheader("데이터 미리보기")

# width="stretch" 적용 (최신 버전 대응)
st.dataframe(df, width="stretch")
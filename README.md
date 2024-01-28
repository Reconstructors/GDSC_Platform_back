# GDSC Platform backend
## 환경설정
- conda create -n env_name python=3.10
- conda activate env_name
- pip install -r requirements.txt

## 로컬 서버 구동
- uvicorn sql_app.main:app --reload

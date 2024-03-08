# GDSC Platform backend

## 환경설정

- conda create -n env_name python=3.10
- conda activate env_name
- pip install -r requirements.txt

## 로컬 서버 구동

- uvicorn main:app --reload

- https://wikidocs.net/176073 참고

alembic revision --autogenerate

alembic upgrade head
https://fastapi.tiangolo.com/tutorial/security/get-current-user/

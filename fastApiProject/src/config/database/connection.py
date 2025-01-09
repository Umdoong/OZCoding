from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

DATABASE_URL = "mysql+pymysql://root:be7-fastapi-pw@localhost:33060/be7-fastapi"

engine = create_engine(DATABASE_URL)

# sqlalchemy는 서버와 db 사이에서 정보를 교환할 때 session으로 교환한다
SessionFactory = sessionmaker(
	bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)

# 세션 열고 닫아주는 함수
def get_db():
	session = SessionFactory()
	try:
		# yield -> 호출한 쪽으로 이동해서 실행을 끝내고 돌아옴
		yield session
	finally:
		session.close()
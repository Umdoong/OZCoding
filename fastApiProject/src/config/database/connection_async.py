from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "mysql+aiomysql://root:be7-fastapi-pw@localhost:33060/be7-fastapi"

async_engine = create_async_engine(DATABASE_URL)

# 그래서 대문자로 시작
AsyncSessionFactory = async_sessionmaker( # 얘는 호출될 때 클레스를 만들어 줌
	bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False,
)

async def get_async_db():
	session = AsyncSessionFactory()
	try:
		yield session
	finally:
		await session.close() # db로 Connection 종료 보내는데 대기 발생
from fastapi import Depends
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from config.database.connection_async import get_async_db
from users.models import User


class UserAsyncRepository:
	def __init__(self, db: AsyncSession = Depends(get_async_db)):
		self.db = db

	async def save(self, user: User) -> None:
		self.db.add(user)
		await self.db.commit()

	async def get_users(self):
		result = await self.db.execute(select(User))
		return result.scalars().all()# scalars: 데이터 -> ORM(USER)객체
	# async 함수라서 반환이 코루틴(작업)임

	async def username_exists(self, username: str) -> bool:
		result = await self.db.execute(
			select(exists().where(User.username == username))
		) # exists: 유저가 있으면 True
		return result.scalar() # 단일 값이라 scalar

	# 이것도 오버헤드가 크진 않지만 검사만 하면 되기 때문에 return값이 필요없다
	# async def get_user_by_username(self, username: str) -> User | None:
	# 	result = await self.db.execute(
	# 		select(User).where(User.username == username)
	# 	)
	# 	return result.scalars().first()

	async def get_user_by_id(self, user_id: int) -> User | None:
		result = await self.db.execute(
			select(User).where(User.id == user_id)
		)
		return result.scalars().first()

	async def delete(self, user: User) -> None:
		await self.db.delete(user) # add랑 다르게 delete할 거 db에 마크해놓음
		await self.db.commit()
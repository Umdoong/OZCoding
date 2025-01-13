from typing import Sequence

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from config.database.connection import get_db
from users.models import User
from users.password import is_bcrypt_pattern


class UserRepository:
	def __init__(self, db: Session = Depends(get_db)):
		self.db = db

	# db에 유저 추가 후 커밋하는 함수
	def save(self, user: User) -> None:
		self.db.add(user)
		assert is_bcrypt_pattern(user.password), "진짜 레전드 상황 발생"
		self.db.commit()

	# 모든 유저를 가져오는 함수
	def get_users(self) -> list[User]: # sequence => str, list, tuple
		result = self.db.execute(select(User))
		return result.scalars().all() # noqa -> 노란줄 무시 주석
		# 원래 list로 반환되는데 sqlalchemy에서 sequence로 힌팅해놔서 노란 줄 뜨는 것!

	def get_user_by_username(self, username: str) -> User | None:
		result = self.db.execute(select(User).where(User.username == username))
		return result.scalars().first()

	def get_user_by_id(self, user_id: int) -> User | None:
		result = self.db.execute(select(User).where(User.id == user_id))
		return result.scalars().first()

	def delete(self, user: User) -> None:
		user.remove_profile_image()
		self.db.delete(user)
		self.db.commit() # delete 후 commit 해줘야 함
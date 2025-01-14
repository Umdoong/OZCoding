import os, uuid, shutil, aiofiles
from aiofiles import os as aiofiles_os
from fastapi import UploadFile
from config.database.orm import Base
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime

from users.password import is_bcrypt_pattern


class User(Base):
	__tablename__ = 'service_user'

	id = Column(Integer, primary_key=True)
	username = Column(String(16), nullable=False)
	password = Column(String(60), nullable=False) # bcrypt 최대 60자
	profile_image = Column(String(100), nullable=True)
	created_at = Column(DateTime, nullable=False, default=datetime.now)

	__table_args__ = (
		UniqueConstraint("username", name="uix_service_user_username"),# uix=unique index
	)

	@classmethod
	# 객체를 만드는 메소드
	def create(cls, username: str, password: str) -> 'User':
		# assert: 500번대 오류가 생김, 발생하면 안되는 상황
		assert is_bcrypt_pattern(password=password), "Invalid password pattern" # message log에만 찍힘
		return cls(	username=username, password=password)

	# instance method / 객체를 직접 수정하니까
	def update_password(self, password: str) -> None:
		assert is_bcrypt_pattern(password=password), "Invalid password pattern" # message log에만 찍힘
		self.password = password

	# 동기
	# def remove_profile_image(self):
	# 	if self.profile_image:
	# 		os.remove(self.profile_image)

	# def upload_profile_image(self, profile_image: UploadFile):
	# 	self.remove_profile_image()
	#
	# 	# uuid는 임의의 중복되지 않는 패턴을 만들어주는 알고리즘
	# 	unique_filename: str = f"{uuid.uuid4()}_{profile_image.filename}"
	#
	# 	# file_path => users/images/{unique_filename}
	# 	file_path: str = os.path.join("users/images", unique_filename)
	# 	with open(file_path, "wb") as f:
	# 		shutil.copyfileobj(profile_image.file, f)
	#
	# 	self.profile_image = file_path

	async def remove_profile_image(self):
		if self.profile_image:
			aiofiles_os.remove(self.profile_image)

	async def upload_profile_image(self, profile_image: UploadFile):
		await self.remove_profile_image()

		unique_filename: str = f"{uuid.uuid4()}_{profile_image.filename}"

		file_path: str = f"users/images/{unique_filename}"

		async with aiofiles.open(file_path, "wb") as f:
			while chunk := await profile_image.read(1024 * 4):
				await f.write(chunk)

		self.profile_image = file_path


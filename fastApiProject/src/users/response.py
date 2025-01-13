from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class UserResponse(BaseModel):
	id: int
	name: str
	date_of_birth: date
	profile_image: str | None
	model_config = ConfigDict(from_attributes=True)




class UserMeResponse(BaseModel):
	id: int
	username: str
	password: str
	profile_image: str | None
	model_config = ConfigDict(from_attributes=True)


class UserResponseAuth(BaseModel):
	id: int
	username: str
	created_at: datetime
	model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
	users: list[UserResponseAuth]
	model_config = ConfigDict(from_attributes=True)

class UserMeResponseAuth(BaseModel):
	id: int
	username: str
	password: str
	created_at: datetime

	# dict말고 attributes도 가능하게 해줌 / attributes => 객체에 .찍어서 정보 받아오는 거
	model_config = ConfigDict(from_attributes=True)

class JWTResponse(BaseModel):
	access_token: str
	model_config = ConfigDict(from_attributes=True)


from pydantic import BaseModel
from datetime import date

class UserResponse(BaseModel):
	id: int
	name: str
	date_of_birth: date
	image: str | None = None


class UserListResponse(BaseModel):
	users: list[UserResponse]


class UserMeResponse(BaseModel):
	id: int
	username: str
	password: str
	name: str
	date_of_birth: date
	image: str | None = None


class UserResponseAuth(BaseModel):
	id: int
	username: str


class UserMeResponseAuth(BaseModel):
	id: int
	username: str
	password: str


class JWTResponse(BaseModel):
	access_token: str
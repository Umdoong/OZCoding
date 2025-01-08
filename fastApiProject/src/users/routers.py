import os, uuid, shutil
from datetime import date

from fastapi.security.http import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, UploadFile, status, HTTPException, Depends
from fastapi.responses import *

from .authentication import create_access_token
from .exceptions import UserNotFoundException, UserProfileImageNotFoundException, UserIncorrectPasswordException
from .request import *
from .response import *
from .password import hash_password, check_password

router = APIRouter(tags=["Users"])

users = [
	{"id": 1, "username": "elon", "password": "musk123", "name": "Elon Musk", "date_of_birth": date(1970, 1, 1), "image": "684325e1-5a9c-4ad0-b226-09cdb1193bb4_IMG_3599.jpg"},
	{"id": 2, "username": "melon", "password": "musk456", "name": "Melon Musk", "date_of_birth": date(2000, 1, 1)}
		 ]

users_auth = [
	{"id": 1, "username": "elon", "password": "$2b$12$u597ZBtbJ5f5YD7.SBQjzOPRR9/EMi.2.zMkjuK7EB6pVHPGkhMq2"},
	{"id": 2, "username": "melon", "password": "$2b$12$pWAxz3GUJdVjNgaT1M9YneumVLrQljQHx88yZqINL0FZsVocgbQES"}
]

# 전체 유저 목록 조회 API
@router.get('/users', status_code=status.HTTP_200_OK)
def get_users_handler():
	return UserListResponse.model_validate({"users": users})
	# ==
	# return UserListResponse(
	# 	users=[UserResponse(**user) for user in users]
	# )


# C: 새로운 유저 생성 API
@router.post('/users',
			 status_code=status.HTTP_201_CREATED,
			 response_model=UserResponse,
			 )
def create_user_handler(body: UserCreateRequestBody):
	# 1. 사용자로부터 데이터를 받고
	# 2. 받은 데이터의 유효성 검사
	# 3. 새로운 유저 데이터를 유저 목록에 추가
	new_user ={
		"id": len(users) + 1,
		"name": body.name,
		"date_of_birth": body.date_of_birth,
	}
	users.append(new_user)
	return UserResponse.model_validate(new_user) # model_validate를 쓰면 딕셔너리 자체를 넘길 수 있음


# C: 비밀번호 해쉬화
@router.post(
	'/users/hash',
			 status_code=status.HTTP_201_CREATED,
			response_model=UserMeResponseAuth
)
def create_user_hash_handler(body: UserCreateRequestBodyAuth):
	new_user ={
		"id": len(users_auth) + 1,
		"username": body.username,
		"password": hash_password(plain_text=body.password)
	}
	users_auth.append(new_user)
	return UserMeResponseAuth.model_validate(new_user) # model_validate를 쓰면 딕셔너리 자체를 넘길 수 있음


basic_auth = HTTPBasic()

# R: 로그인
@router.get(
	"/users/login",
	status_code=status.HTTP_200_OK,
	response_model=JWTResponse
)
def user_login_handler(credentials: HTTPBasicCredentials = Depends(basic_auth)):
	# Basic Auth 이용해서 Header로 credentials -> 비밀번호 확인 -> access_token(JWT) 발급
	for user in users_auth:
		if credentials.username == user["username"]:
			if check_password(plain_text=credentials.password, hashed_password=user["password"]):
				print(user['id'])
				return JWTResponse(access_token=create_access_token(user_id=user["id"]))
			raise UserIncorrectPasswordException
	raise UserNotFoundException



# R: 내 정보 조회 API
@router.get(
	"/users/me",
	status_code=status.HTTP_200_OK,
	response_model=UserMeResponseAuth
)
def get_me_handler(credentials: HTTPBasicCredentials = Depends(basic_auth)):
	# credentials.password => Authrization: Basic header로 넘기는 password
	# user["password"] => 평문

	for user in users_auth:
		if credentials.username == user["username"]:
			if check_password(plain_text=credentials.password, hashed_password=user["password"]):
				return UserMeResponseAuth.model_validate(user)
			raise UserIncorrectPasswordException
	raise UserNotFoundException


# R: 특정 유저 조회 API
@router.get('/users/{user_id}',
			status_code=status.HTTP_200_OK,
			response_model=UserResponse,
			)
def get_user_handler(user_id: int):
	for user in users:
		if user["id"] == user_id:
			return UserResponse.model_validate(user)
	raise UserNotFoundException

# U: 유저 정보 업데이트 API
@router.patch('/users/{user_id}',
			  status_code=status.HTTP_200_OK,
			  response_model=UserResponse,
			  )
def update_user_handler(user_id: int, body: UserUpdateRequestBody):
	for user in users:
		if user["id"] == user_id:
			user["name"] = body.name
			return UserResponse.model_validate(user)

	raise UserNotFoundException


# U: 사용자 프로필 이미지 업데이트 API
@router.post('/users/{user_id}/images',
			 status_code=status.HTTP_201_CREATED,
			response_model = UserResponse,
			)
def update_profile_image_handler(user_id: int, profile_image: UploadFile):
	for user in users:
		if user["id"] == user_id:
			# uuid는 임의의 중복되지 않는 패턴을 만들어주는 알고리즘
			unique_filename = f"{uuid.uuid4()}_{profile_image.filename}"

			# file_path => users/images/{unique_filename}
			file_path = os.path.join("users/images", unique_filename)
			#
			with open(file_path, "wb") as f:
				shutil.copyfileobj(profile_image.file, f)

			user["image"] = unique_filename
			return UserResponse.model_validate(user)
	raise UserNotFoundException


# R: 이미지 다운로드 API
@router.get("/users/{user_id}/images/download",
			status_code=status.HTTP_200_OK,
			response_model=None,
			)
def download_profile_image_handler(user_id: int):
	for user in users:
		if user["id"] == user_id:
			if image := user.get("image"): # 월러스
				file_path = os.path.join("users/images", image)
				original_filename = "".join(file_path.split("_")[1:])
				return FileResponse(
					file_path, # 타입을 추론해서 줌
					headers={"Content-Disposition": f"attachment; filename={original_filename}"} # 다운로드 할 수 있음
				)
			raise UserProfileImageNotFoundException
	raise UserNotFoundException


# D: 유저 삭제 API
@router.delete('/users/{user_id}',
			   status_code=status.HTTP_204_NO_CONTENT,
			   response_model=None,
			   )
def delete_user_handler(user_id: int):
	for user in users:
		if user["id"] == user_id:
			users.remove(user)
			return users
	raise UserNotFoundException

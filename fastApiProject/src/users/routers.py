import os, uuid, shutil
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi.security.http import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, UploadFile, status, HTTPException, Depends, Body, File
from fastapi.responses import *

from config.database.connection import SessionFactory, get_db
from .authentication import create_access_token, verify_access_token, authenticate
from .exceptions import UserNotFoundException, UserProfileImageNotFoundException, UserIncorrectPasswordException, \
	DuplicateUsernameException
from .models import User
from .repository import UserRepository
from .request import *
from .response import *
from .password import hash_password, check_password

router = APIRouter(tags=["Users"])

basic_auth = HTTPBasic()
bearer_auth = HTTPBearer()

# 전체 유저 목록 조회 API
@router.get('/users', status_code=status.HTTP_200_OK)
def get_users_handler(
		_: int = Depends(authenticate),
		user_repo: UserRepository = Depends(UserRepository),
):
	users = user_repo.get_users()
	return UserListResponse.model_validate({"users": users}) # model_validate를 쓰면 딕셔너리 자체를 넘길 수 있음


# C: 새로운 유저 생성 API
@router.post('/users',
			 status_code=status.HTTP_201_CREATED,
			 response_model=UserMeResponseAuth,
			 )
def create_user_handler(
		body: UserCreateRequestBodyAuth,
		user_repo: UserRepository = Depends(), # 힌팅의 클래스와 의존하는 클래스 명이 같으면 Depends 괄호 내용 생략 가능
):
	# 1. 사용자로부터 데이터를 받고
	# 2. 받은 데이터의 유효성 검사
	# 3. 새로운 유저 데이터를 유저 목록에 추가

	if user_repo.get_user_by_username(username=body.username):
		raise DuplicateUsernameException

	new_user = User.create(username=body.username, password=hash_password(plain_text=body.password))
	try: # 2중으로 예외 처리
		user_repo.save(user=new_user) # 이전엔 id가 None이었다가 commit되는 순간 PK가 생성됨
	except IntegrityError: # 데이터가 오염되지 않았는지
		raise DuplicateUsernameException
	return UserMeResponseAuth.model_validate(new_user)


# C: 사용자 프로필 이미지 업데이트 API
@router.post('/users/me/images',
			status_code=status.HTTP_201_CREATED,
			response_model = UserMeResponse,
			 )
def upload_profile_image_handler(
		user_id: int = Depends(authenticate),
		profile_image: UploadFile = File(),
		user_repo: UserRepository = Depends(UserRepository)
):
	if not (user := user_repo.get_user_by_id(user_id=user_id)):
		raise UserNotFoundException

	user.upload_profile_image(profile_image=profile_image)
	user_repo.save(user=user)
	return UserMeResponse.model_validate(user)


# R: 이미지 다운로드 API
@router.get(
	"/users/{user_id}/images",
			status_code=status.HTTP_200_OK,
			response_model=None,
			)
def download_profile_image_handler(
		user_id: int,
		me_id: int = Depends(authenticate),
		user_repo: UserRepository = Depends()
):

	if not (user := user_repo.get_user_by_id(user_id=user_id)):
		raise UserNotFoundException

	if not user.profile_image:
		raise UserProfileImageNotFoundException

	return FileResponse(user.profile_image)


# R: 로그인
@router.get(
	"/users/login",
	status_code=status.HTTP_200_OK,
	response_model=JWTResponse
)
def user_login_handler(
		credentials: HTTPBasicCredentials = Depends(basic_auth),
		user_repo: UserRepository = Depends(UserRepository),
):
	# Basic Auth 이용해서 Header로 credentials -> 비밀번호 확인 -> access_token(JWT) 발급
	if not (user:= user_repo.get_user_by_username(username=credentials.username)):
		raise UserNotFoundException
	if not (check_password(plain_text=credentials.password, hashed_password=user.password)):
		raise UserIncorrectPasswordException
	return JWTResponse(access_token=create_access_token(user_id=user.id))


# R: 내 정보 조회 API (BASIC)
@router.get(
	"/users/me",
	status_code=status.HTTP_200_OK,
	response_model=UserMeResponseAuth
)
def get_me_handler(credentials: HTTPBasicCredentials = Depends(basic_auth)):
	# credentials.password => Authrization: Basic header로 넘기는 password
	# user["password"] => 평문

	users_auth = [
		{"id": 1, "username": "elon", "password": "$2b$12$u597ZBtbJ5f5YD7.SBQjzOPRR9/EMi.2.zMkjuK7EB6pVHPGkhMq2"},
		{"id": 2, "username": "melon", "password": "$2b$12$pWAxz3GUJdVjNgaT1M9YneumVLrQljQHx88yZqINL0FZsVocgbQES"}
	]
	for user in users_auth:
		if credentials.username == user["username"]:
			if check_password(plain_text=credentials.password, hashed_password=user["password"]):
				return UserMeResponseAuth.model_validate(user)
			raise UserIncorrectPasswordException
	raise UserNotFoundException


# R: 내 정보 조회 API (BEARER)
@router.get(
	"/users/me/jwt",
	status_code=status.HTTP_200_OK,
	response_model=UserMeResponseAuth
)
def get_me_jwt_handler(
		me_id: int = Depends(authenticate), # 토큰
		user_repo: UserRepository = Depends(UserRepository),
):
	if not (user := user_repo.get_user_by_id(user_id=me_id)):
		raise UserNotFoundException
	return UserMeResponseAuth.model_validate(user)


# R: 특정 유저 조회 API
@router.get('/users/{user_id}',
			status_code=status.HTTP_200_OK,
			response_model=UserResponse,
			)
def get_user_handler(
		user_id: int,
		user_repo: UserRepository = Depends(UserRepository),
):
	if not (user := user_repo.get_user_by_id(user_id=user_id)):
		raise UserNotFoundException
	return UserResponse.model_validate(user)


# U: 내 정보 업데이트 API
@router.patch('/users/me/jwt',
			  status_code=status.HTTP_200_OK,
			  response_model=UserMeResponseAuth,
			  )
def update_user_handler(
		# 먼저 동작해야하는 코드부터 앞에
		me_id: int = Depends(authenticate), # HTTP header
		body: UserUpdateRequestBody = Body(), # body
		user_repo: UserRepository = Depends(UserRepository),
):
	if not (user := user_repo.get_user_by_id(user_id=me_id)):
		raise UserNotFoundException

	user.update_password(password=hash_password(plain_text=body.password))
	user_repo.save(user=user)
	return UserMeResponseAuth.model_validate(user)


# D: 유저 삭제 API
@router.delete(
		'/users/me/jwt',
		status_code=status.HTTP_204_NO_CONTENT,
		response_model=None,
)
def delete_user_handler(
		user_id: int = Depends(authenticate),
		user_repo: UserRepository = Depends(),
):
	if not (user := user_repo.get_user_by_id(user_id=user_id)):
		raise UserNotFoundException

	user_repo.delete(user=user)
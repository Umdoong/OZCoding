from http.client import HTTPException
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, status, UploadFile, File

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database.connection_async import get_async_db
from .authentication import authenticate
from .exceptions import DuplicateUsernameException, UserNotFoundException
from .models import User
from .password import hash_password
from .repository_async import UserAsyncRepository
from .request import UserCreateRequestBodyAuth
from .response import UserListResponse, UserMeResponseAuth, UserMeResponse

# 비동기 핸들러

router = APIRouter(prefix="/async")

@router.get(
	"/users",
	status_code=status.HTTP_200_OK,
	response_model=UserListResponse
)

# R: 전체 유저 조회
async def get_users_handler(
		_: int =Depends(authenticate), # 의존성 내에도 대기가 발생하면 async함수 따로 만들어야함
		user_repo: UserAsyncRepository = Depends(),
):
	# 코루틴을 반환받아야해서 await 써줘야함
	users = await user_repo.get_users() # 안에서 멈추면 밖에서도 멈춰줘야 한다고 생각하면 편함
	return UserListResponse.model_validate({"users": users})

# C: 새로운 유저 생성 API
@router.post('/users',
			 status_code=status.HTTP_201_CREATED,
			 response_model=UserMeResponseAuth,
			 )
async def create_user_handler(
		body: UserCreateRequestBodyAuth,
		# db: AsyncSession = Depends(get_async_db),
		user_repo: UserAsyncRepository = Depends(),
):

	if user_repo.username_exists(username=body.username):
		raise DuplicateUsernameException

	new_user = User.create(username=body.username, password=hash_password(plain_text=body.password))
	await user_repo.save(new_user)
	return UserMeResponseAuth.model_validate(new_user)

# C: 사용자 프로필 이미지 업데이트 API
@router.post('/users/me/images',
			status_code=status.HTTP_201_CREATED,
			response_model = UserMeResponse,
			 )
async def upload_profile_image_handler(
		user_id: int = Depends(authenticate),
		profile_image: UploadFile = File(),
		user_repo: UserAsyncRepository = Depends(),
):
	if not (user := await user_repo.get_user_by_id(user_id=user_id)):
		raise UserNotFoundException
	old_path = user.profile_image
	await user.upload_profile_image(profile_image=profile_image)
	try:
		await user_repo.save(user=user)
	except IntegrityError:
		await user.remove_profile_image() # 새로운 프로필 삭제
		user.profile_image = old_path
		await user_repo.save(user=user)
		raise HTTPException("이미지 업로드 실패")
	return UserMeResponse.model_validate(user)
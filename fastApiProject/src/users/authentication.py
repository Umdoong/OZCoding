import jwt, time
from jwt.exceptions import InvalidTokenError

from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from users.exceptions import *

from typing import TypedDict


# TypedDict로 dict의 키와 type을 정해줄 수 있다
class JWTPayload(TypedDict):
	user_id: int
	isa: float


JWT_SECRET_KEY = "d5d30a7575cd0a19f5e2fbe476ca43bc46ad5aa70b7f06003a6f78d20662f412"
JWT_ALGORITHM = "HS256"

# 1. 로그인 성공한 유저에게 access_token 생성해서 발급하는 함수
def create_access_token(user_id: int) -> str:
	# JWT = Header + Payload + Signature
	payload: JWTPayload = {"user_id": user_id, "isa": time.time()} # isa => issued at
	access_token = jwt.encode(
		payload=payload,
		key=JWT_SECRET_KEY, # 터미널에 openssl rand -hex 32 치면 랜덤 수 만들어줌
		algorithm=JWT_ALGORITHM,
	)
	return access_token

# 2. access_token을 검증하고, payload를 꺼내는 함수
def verify_access_token(access_token: str):
	try:
		payload: JWTPayload = jwt.decode(
			jwt=access_token,
			key=JWT_SECRET_KEY,
			algorithms=[JWT_ALGORITHM],
		)
	except InvalidTokenError:
		raise InvalidJWTException

	issued_at: float = payload.get("isa", 0)
	if issued_at + (60 * 60 * 24 * 7) < time.time():
		raise JWTExpiredException

	return payload["user_id"] # -> 없는 key 입력하면 keyError 반환, get으로 가져올 때는 key 없으면 None 반환


bearer_auth = HTTPBearer()

def authenticate(
	auth_header: HTTPAuthorizationCredentials = Depends(bearer_auth),
):
	access_token: str = auth_header.credentials
	user_id: int = verify_access_token(access_token=access_token)
	return user_id
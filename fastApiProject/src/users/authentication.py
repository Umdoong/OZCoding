import jwt, time
from users.exceptions import JWTExpiredException

JWT_SECRET_KEY = "d5d30a7575cd0a19f5e2fbe476ca43bc46ad5aa70b7f06003a6f78d20662f412"
JWT_ALGORITHM = "HS256"

# 1. 로그인 성공한 유저에게 access_token 생성해서 발급하는 함수
def create_access_token(user_id: int) -> str:
	# JWT = Header + Payload + Signature
	payload = {"user_id": user_id, "isa": time.time()} # isa => issued at
	access_token = jwt.encode(
		payload=payload,
		key=JWT_SECRET_KEY, # 터미널에 openssl rand -hex 32 치면 랜덤 수 만들어줌
		algorithm=JWT_ALGORITHM,
	)
	return access_token

# 2. access_token을 검증하고, payload를 꺼내는 함수
def verify_access_token(access_token: str):
	payload = jwt.decode(
		token=access_token,
		key=JWT_SECRET_KEY,
		algorithms=[JWT_ALGORITHM],
	)
	issued_at: float = payload.get("isa", 0)
	if issued_at + (60 * 60 * 24) < time.time():
		raise JWTExpiredException

	return payload["user_id"] # -> 없는 key 입력하면 keyError 반환, get은 없으면 None 반환
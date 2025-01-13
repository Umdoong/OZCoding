import bcrypt, re

def hash_password(plain_text: str) -> str:
	hashed_password_bytes: bytes = bcrypt.hashpw(plain_text.encode('utf-8'), bcrypt.gensalt())
	return hashed_password_bytes.decode('utf-8')

def check_password(plain_text: str, hashed_password: str) -> bool:
	return bcrypt.checkpw(
		plain_text.encode('utf-8'), # 사용자로부터 넘겨 받은 평문
		hashed_password.encode('utf-8') # 서버에 보관 중인 비밀번호 해시 값
	)

def is_bcrypt_pattern(password: str) -> bool:
	bcrypt_pattern = r'^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$'
	return re.match(bcrypt_pattern, password) is not None
# Regular Expression(정규식 표현) -> re(python standard lib)
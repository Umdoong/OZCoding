from fastapi import HTTPException, status

# HTTPException을 사용, HTTP -> ㄱ
# UserNotFoundException = HTTPException(
# 	status_code=status.HTTP_404_NOT_FOUND,
# 	detail="User not found"
# )
#
# UserProfileImageNotFoundException = HTTPException(
# 	status_code=status.HTTP_404_NOT_FOUND,
# 	detail="User profile image not found"
# )

UserIncorrectPasswordException = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Incorrect username or password",
)

JWTExpiredException = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="JWT expired",
)

InvalidJWTException = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Invalid JWT",
)

DuplicateUsernameException = HTTPException(
	status_code=status.HTTP_409_CONFLICT, # 데이터가 충돌난다
	detail="Username already exists"
)

# exception custom
class UserNotFoundException(Exception):
	detail = "User not found"

class UserProfileImageNotFoundException(Exception):
	detail = "User profile image not found"
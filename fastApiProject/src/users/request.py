from pydantic import BaseModel, field_validator
from datetime import date, timedelta

class UserCreateRequestBody(BaseModel):
	name: str
	date_of_birth: date

	@field_validator("date_of_birth")
	def validate_date_of_birth(cls, v): # 클래스 메소드라 cls 받아와야함
		age_delta = date.today() - v
		if age_delta.days < 5 * 365:
			raise ValueError("만 6세 이상만 가입할 수 있습니다.")
		return v # 규칙임 해야됨 데코레이터 내부에서 써야 작동되게 해놨음

# validationError => 모든 유효성 검사를 끝내고 최종적으로 나오는 에러

"""
클래스 메소드, 인스턴스 메소드, 정적메소드 나중에 찾아볼 것
class Test:
	#클래스 메소드
	def foo(cls):
		return
		
	#인스턴스 메소드
	def boo(self):
		return
		
Test().foo
test = Test()
test.boo
"""

class UserUpdateRequestBody(BaseModel):
	username: str


class UserCreateRequestBodyAuth(BaseModel):
	username: str
	password: str
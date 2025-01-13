from http.client import responses

from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from datetime import datetime

from items.routers import router as items_router
from users.routers import router as users_router # as = alias
from users.exceptions import UserNotFoundException

# pydantic: 데이터 유효성 검사를 하기 위한 라이브러리
# BaseModel: 우리가 직접 검증할 데이터를 선언해서 사용할 때
# fastapi: Query, Body 등은 이미 만들어둔 거
app = FastAPI()

# app과 router를 연결시켜줌
app.include_router(items_router)
app.include_router(users_router)

@app.get("/now")
def get_now_handler():
	# Response는 미디어 타입을 명시 해줄 수 있음
	return Response(
		content=str(datetime.now()), # str로 안해주면 객체라서 못읽음
		media_type="text/plain",
		status_code=200,
	)
	# python datetime 객체 -> JSON String / JSON은 알아서 직렬화 역직렬화 해줌
	# return {"now": datetime.now()}


@app.get("/now/html")
def get_now_html_handler():
	html = f"<html><body><h1>now: {datetime.now()}</h1></body></html>"
	# == Response(media_type="text/html", content=html)
	return HTMLResponse(content=html)



class NowResponse(BaseModel):
	now: datetime
	# field: 타입

# response_model => swagger에서 예시와 스키마가 표시됨
@app.get("/now/test", response_model=NowResponse)
def get_now_test_handler():
	return NowResponse(now=datetime.now()) # => JSON형태, pydantic의 유효성 검사를 해주면서 반환 가능



# 도메인
# e-커머스(쿠팡) -> 큰 도메인
# 회원. 상품, 주문, 결제, 광고 => 논리적으로 비슷한 애들끼리 묶어놓고 관리
# 이런식으로 패키지를 관리

############################################################################

# exception 오버라이딩
@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request: Request, exc: RequestValidationError):
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={'detail': jsonable_encoder(exc.errors())}
	)

# exception 커스텀
@app.exception_handler(UserNotFoundException) # exception_handler에서 setdefault 검색하면 각 handler 디폴트 검색 가능
def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={'detail': exc.detail}
	)

# AssertionError 클라이언트 쪽에 보여주고 싶을 때
@app.exception_handler(AssertionError)
def assert_exception_handler(_: Request, exc: AssertionError):
	return JSONResponse(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={'detail': str(exc)}
	)


# salt는 같은 입력값을 넣어도 결과값이 달라짐 (bcrypt.checkpw로 확인 가능)
# salt를 이용해서 brute-force를 방지
# -> db가 털렸을 때 brute-force로 해쉬값을 찾아낼 때 salt를 사용하면 같은 해쉬 결과값을 찾아내기가 매우 힘들어진다.


#################비동기#################
import asyncio, time, httpx

@app.get("/sync/json")
async def sync_json_hander():
	start_time = time.perf_counter()
	urls = [
		"https://jsonplaceholder.typicode.com/posts",
		"https://jsonplaceholder.typicode.com/posts",
		"https://jsonplaceholder.typicode.com/posts"
	]
	responses = []
	for url in urls:
		responses.append(httpx.get(url).json())

	end_time = time.perf_counter()
	return {
		"duration": end_time - start_time,
		"responses": responses
	}


@app.get("/async/json")
async def async_json_hander():
	start_time = time.perf_counter()
	urls = [
		"https://jsonplaceholder.typicode.com/posts",
		"https://jsonplaceholder.typicode.com/posts",
		"https://jsonplaceholder.typicode.com/posts"
	]
	async with httpx.AsyncClient() as client:
		tasks = []
		for url in urls:
			tasks.append(client.get(url))
		responses = await asyncio.gather(*tasks)

		# 코루틴 객체에서 json을 호출해줘야함
		result = []
		for res in responses:
			result.append(res.json())

	end_time = time.perf_counter()
	return {
		"duration": end_time - start_time,
		"responses": result
	}
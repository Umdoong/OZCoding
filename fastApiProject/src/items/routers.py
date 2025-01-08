from fastapi import APIRouter, Query, Path


# prefix: 모든 경로 앞에 붙이고 싶은 거
# tags: swagger에서 라우트별로 구분하고 싶을 때
# include_in_schema=False: swagger에서 보여주고 싶지 않을 때, 특정 API만 적용도 가능
# deprecated=True: 아직은 쓸 수 있는데 다음 버전에서 없어질 API
# todo: 2025-01-01 삭제

router = APIRouter(prefix="/api/v1/items", tags=["Items"], include_in_schema=True)

items = [
	{"id": 1, "name": "i-phone 16", "price": 100},
	{"id": 2, "name": "Galaxy 25", "price": 200},
	{"id": 3, "name": "Huawei", "price": 50},
]

# Query Param : 127.0.0.1:8000/test?price_lt=10000, ?key=value
# lt: less than = 미만
# gt: greater than = 초과
# lte, le: less than or equal to = 이하
# gte, ge: greater than or equal to = 이상

@router.get("/test", include_in_schema=False, deprecated=True)
def test_handler(price_lt: int | None = None): # default를 None으로 해줬기 때문에 타입힌트를 int | None으로 쓴 것
	# default 값 없으면 필수값(required)으로 해석
	# Optional한 값으로 처리하고 싶으면, default를 넣어서 값을 넣거나 안넣거나
	if price_lt:
		# 가격이 10000원 미만인 상품만 찾아서 반환
		return {"Query Param": price_lt}
	else:
		# return 전체 상품
		return items


# 전체 상품 목록
# 127.0.0.1:8000/items?min_price=100&max_price=200
@router.get("")
def items_handler(
		min_price: int | None = None,
		max_price: int | None = None,
):
	# price_gte = max_price 의미가 같아서 둘 중 하나를 골라서 사용
	result = items
	if min_price:
		# 가격이 min_price 이상인 상품 조회
		result = [item for item in result if item["price"] >= min_price]

	if max_price:
		# 가격이 max_price 이하인 상품 조회
		result = [item for item in result if item["price"] <= max_price]

	return {"items": result}

# 특정 상품 반환
# RESTful 관용적인 건데 물건같은 명사는 보통 복수형을 사용한다
# Path Param : path에서 값을 가져옴

# Query로 좀 더 디테일하게 가능, 숫자에 _는 선택
# max_price: int | None = Query(None, ge=10_000, lt=1_000_000)

# 필수값으로 Query를 받고 싶을 때
# max_price: int = Query(..., ge=10_000, lt=1_000_000) / default 쪽에 ...
# max_length(최대 길이), max_digits(최대 자릿수)

@router.get("/{item_id}")
def item_handler(
		item_id: int, # path 변수
		# item_id: int = Path(..., max_digits=5) / Path class 이용 가능
		# query param / path와 같이 쓸 수 있다
		max_price: int | None = None,
		keyword: str | None = Query(None, max_length=5),
):
	result = None
	for item in items:
		if item["id"] == item_id:
			result = item

	return {"item": result}


# /categories/{category_name}
# 127.0.0.1:8000/categories/pants?min_price=10000&max_price=50000
# -> category_name이 pants인 상품에 대해서 가격 1~5만원 조회
# 네이버 쇼핑 /search?query=팬츠&priceRange=6000~10000
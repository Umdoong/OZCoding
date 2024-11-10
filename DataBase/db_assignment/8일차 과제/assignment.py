from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.local

# [문제 1 특정 장르의 책 찾기]
# 문제 설명
# 데이터베이스에 새로운 필드로 `genre`를 책 데이터에 추가하였습니다. 사용자는 "fantasy" 장르의 모든 책을 찾고 싶어합니다.
# - 쿼리 작성 목표
# "fantasy" 장르에 해당하는 모든 책의 제목과 저자를 찾는 MongoDB 쿼리를 함수로 만들어 문제를 해결해 봅니다.

# 주어진 DB insert에 장르가 없다..!! 만들어야겠지...?
# db.books.update_one({"title": "Kafka on the Shore"}, {"$set": {"genre": "fantasy"}})
# db.books.update_one({"title": "Norwegian Wood"}, {"$set": {"genre": "Romance"}})
# db.books.update_one({"title": "1Q84"}, {"$set": {"genre": "Dystopian"}})

def find_genre(db, genre):
	books_collection = db.books
	query = {"genre": genre}
	projection = {"_id": 0, "title": 1, "author": 1, "genre": 1}

	books = books_collection.find(query, projection)
	for book in books:
		print(book)

find_genre(db, "fantasy")


# [문제 2 감독별 평균 영화 평점 계산]
# - 문제 설명
# 각 영화 감독별로 그들의 영화 평점의 평균을 계산하고 싶습니다. 이를 통해 어떤 감독이 가장 높은 평균 평점을 가지고 있는지 알아볼 수 있습니다.
# - 쿼리 작성 목표
# 모든 영화 감독의 영화 평점 평균을 계산하고, 평균 평점이 높은 순으로 정렬하는 MongoDB 쿼리를 함수로 만들어 문제를 해결해 봅니다.
def director_avg_raiting(db):
	movies_collection = db.movies
	pipeline = [
		{"$group": {"_id": "$director", "average_raiting": {"$avg": "$rating"}}}, # _id는 고유 식별자
		{"$sort": {"average_raiting": -1}}
	]

	results = movies_collection.aggregate(pipeline)
	for result in results:
		print(result)

director_avg_raiting(db)


# [문제 3 특정 사용자의 최근 행동 조회]
# - 문제 설명
# 특정 사용자의 최근 행동 로그를 조회하고자 합니다. 이 때, 최신 순으로 정렬하여 최근 5개의 행동만을 보고 싶습니다.
# - 쿼리 작성 목표
# 사용자 ID가 1인 사용자의 최근 행동 5개를 시간 순으로 정렬하여 조회하는 MongoDB 쿼리를 함수로 만들어 문제를 해결해 봅니다.
def find_recent_actions_by_user(db, user_id):
	user_actions_collection = db.user_actions
	query = {"user_id": user_id}
	sort_action = [("timestamp", -1)]

	actions = user_actions_collection.find(query).sort(sort_action).limit(5)
	for action in actions:
		print(action)

find_recent_actions_by_user(db, 1)


# [문제 4 출판 연도별 책의 수 계산]
# - 문제 설명
# 데이터베이스에 저장된 책 데이터를 이용하여 각 출판 연도별로 출판된 책의 수를 계산하고자 합니다. 이 데이터는 시간에 따른 출판 트렌드를 분석하는 데 사용될 수 있습니다.
# - 쿼리 작성 목표
# 각 출판 연도별로 출판된 책의 수를 계산하고, 출판된 책의 수가 많은 순서대로 정렬하는 MongoDB 쿼리를 함수로 만들어 문제를 해결해 봅니다.

def books_by_years(db):
	books_collection = db.books
	pipeline = [
		{"$group": {"_id": "$year", "count": {"$sum": 1}}},
		{"$sort": {"count": -1}},
	]

	results = books_collection.aggregate(pipeline)
	for result in results:
		print(result)

books_by_years(db)


# [문제 5 특정 사용자의 행동 유형 업데이트]
# - 문제 설명
# 특정 사용자의 행동 로그 중, 특정 날짜 이전의 "view" 행동을 "seen"으로 변경하고 싶습니다. 예를 들어, 사용자 ID가 1인 사용자의 2023년 4월 10일 이전의 모든 "view" 행동을 "seen"으로 변경하는 작업입니다.
# - 쿼리 작성 목표
# 사용자 ID가 1인 사용자의 2023년 4월 10일 이전의 "view" 행동을 "seen"으로 변경하는 MongoDB 업데이트 쿼리를 함수로 만들어 문제를 해결해 봅니다.

def update_user_actions_before_date(db, user_id, date, old_action, new_action):
    user_actions_collection = db.user_actions
    query = {"user_id": user_id, "action": old_action, "timestamp": {"$lt": date}}
    update = {"$set": {"action": new_action}}

    result = user_actions_collection.update_many(query, update)
    print(f"Updated {result.modified_count} documents.")

#함수 실행 코드
update_user_actions_before_date(db, 1, datetime(2023, 4, 10), "view", "seen")
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

books = []

# 조회 및 생성
@book_blp.route('/')
class BookList(MethodView):
	@book_blp.response(200, BookSchema(many=True)) # 설정한 스키마로 여러 데이터(many)를 받음
	def get(self):
		return books

	@book_blp.arguments(BookSchema)
	@book_blp.response(201, BookSchema)
	def post(self, new_data):
		new_data['id'] = len(books) + 1 # Auto_Increment를 만들어 줌
		books.append(new_data)
		return new_data

# 조회 및 업데이트, 삭제
@book_blp.route('/<int:book_id>')
class Book(MethodView):
	@book_blp.response(200, BookSchema)
	def get(self, book_id): # books에 있는 책 중 id가 book_id(매개변수)와 같은 데이터가 있으면 조회
		book = next((book for book in books if book['id'] == book_id), None) # next로 book_id가 일치하면 book에 데이터를 할당, 없으면 None을 할당하도록 했다.
		if book is None:
			abort(404, message="Book not found.") # 찾는 book_id가 없으면 404
		return book

	@book_blp.arguments(BookSchema)
	@book_blp.response(200, BookSchema)
	def put(self, new_data, book_id):
		book = next((book for book in books if book['id'] == book_id), None)
		if book is None:
			abort(404, message="Book not found.")
		book.update(new_data) # 위의 get과 비슷하지만 new_data를 추가해준다
		return book

	@book_blp.response(204) # 204 응답에서는 본문 없이 성공 상태만 반환하는 것이 표준, 반환된 데이터를 사용하려면 응답 코드가 200, 202와 같은 데이터 반환용 상태여야 함
	def delete(self, book_id):
		global books # 재할당을 위해 global변수 선언, 없으면 지역변수로 취급되어 메소드가 끝나는 순간 없어진다.
		book = next((book for book in books if book['id'] == book_id), None)
		if book is None:
			abort(404, message="Book not found.")
		books = [book for book in books if book['id'] != book_id] # 매개변수로 입력한 book_id를 제외하고 재할당해준다
		return '' # 없어도 되지만 코드가 성공적으로 실행되었음을 알리는 관례
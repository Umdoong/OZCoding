# Model - 테이블 생성
# user - 사용자
from db import db

class User(db.Model): # db.Model 상속
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	boards = db.relationship('Board', back_populates='author', lazy='dynamic') # db.relationship('클래스명', 역참조 = 'author', / lazy = 'dynamic'->모든 데이터를 가져오지 않고 필요한 해당 쿼리를 실행함)

	# address = db.Column(db.String(120), unique=True, nullable=False)  # 추가된 필드


# boards - 게시글
class Board(db.Model):
	__tablename__ = "boards"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.String(200))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	author = db.relationship('User', back_populates='boards') # User클래스의 boards를 역참조
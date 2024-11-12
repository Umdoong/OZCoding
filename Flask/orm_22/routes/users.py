from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models import User
# Blueprint(name(required.Blueprint 이름 정의), import_name(required.Blueprint의 패키지 이름, 일반적으로 __name__))
user_blp = Blueprint('Users', __name__, description='Operations on users', url_prefix='/users')

# API LIST:
@user_blp.route('/')
class UserList(MethodView):
    def get(self): # (1) 전체 유저 데이터 조회
        users = User.query.all()
        user_data = [{"id":user.id, "name": user.name, "email": user.email} for user in users]  # Convert to list
        return jsonify(user_data)

    def post(self): # (2) 유저 생성
        print("요청은 오는가?")
        user_data = request.json
        new_user = User(name=user_data['name'], email=user_data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201

@user_blp.route('/<int:user_id>')
class UserResource(MethodView):
    def get(self, user_id): # (1) 특정 유저 데이터 조회
        user = User.query.get_or_404(user_id)
        return {"name": user.name, 'email': user.email}

    def put(self, user_id): # (2) 특정 유저 데이터 수정
        user = User.query.get_or_404(user_id)
        user_data = request.json

        user.name = user_data['name']
        user.email = user_data['email']

        db.session.commit()
        return {"message": "User updated"}

    def delete(self, user_id): # (3) 특정 유저 데이터 삭제
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}
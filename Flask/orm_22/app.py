from flask import Flask
from flask_smorest import Api
from db import db
from models import User, Board

app = Flask(__name__) # app 객체 불러오기

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/oz' # db 연결
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 메모리 영역에서 객체가 바뀔 때마다 check할 것이냐 => False
db.init_app(app) # db에 app 전달, db를 다른 곳에서도 연동하기 위해 따로 모듈로 관리

# bluepring 설정 및 등록
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


from routes.users import user_blp
from routes.board import board_blp

api = Api(app) # Api 클래스 객체 생성, api 관리를 위함
api.register_blueprint(user_blp) # user, board 청사진을 api에 등록
api.register_blueprint(board_blp) # Blueprint를 API에 등록하여 해당 라우트가 API의 일부로 작동하도록 설정


from flask import render_template
@app.route('/manage-boards') # 라우트로 경로 설정
def manage_boards(): # View function
    return render_template('boards.html')

@app.route('/manage-users')
def manage_users():
    return render_template('users.html')

if __name__ == '__main__':
    with app.app_context(): # flask에서 application / request context는 자동으로 적용되지만 이렇게 직접 핸들링 할 수 있다
        print("here?") # application context는 앱의 설정과 설정 파일, 데이터베이스 연결 등 애플리케이션 전체에 걸친 리소스를 담고 있다.
        db.create_all() # IF NOT EXISTS와 같은 역할, model이 없으면 만들어라
    app.run(debug=True)
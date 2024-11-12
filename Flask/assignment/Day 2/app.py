from flask import Flask
from flask_smorest import Api
from api import book_blp

app = Flask(__name__)

app.config['API_TITLE'] = 'Book API' # API 이름, swagger UI에 표시될 이름
app.config['API_VERSION'] = 'v1' # API 버전
app.config['OPENAPI_VERSION'] = '3.0.2' # OPEN API 스펙 버전, 원하는 버전으로 하면 됨
app.config['OPENAPI_URL_PREFIX'] = "/" # OPEN API 문서 경로의 기본 URL
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui" # swagger UI의 접근경로
app.config['OPENAPI_SWAGGER_UI_URL'] = "http://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app) # Api 클래스 객체 생성, swagger문서를 비롯한 다양한 api관리 기능 사용 가능
api.register_blueprint(book_blp) # book_blp라는 Blueprint를 API에 등록하여 해당 라우트가 API의 일부로 작동하도록 설정

if __name__ == '__main__':
	app.run(debug=True)

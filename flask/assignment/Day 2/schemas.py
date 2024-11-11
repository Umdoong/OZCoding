from marshmallow import Schema, fields

class BookSchema(Schema):
	id = fields.Int(dump_only=True) # id 필드가 직렬화(즉, Python 객체에서 JSON으로 변환) 과정에서만 사용되고, (서버->클라)
									# 역직렬화(즉, JSON에서 Python 객체로 변환) 과정에서는 무시된다 (클라->서버) 즉, id 값은 서버에서 관리하겠다는 뜻
	title = fields.String(required=True) # 필수로 들어가야 하는 데이터
	author = fields.String(required=True) # 필수2



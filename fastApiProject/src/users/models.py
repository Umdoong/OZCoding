from config.database.orm import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class User(Base):
	__tablename__ = 'service_user'

	id = Column(Integer, primary_key=True)
	username = Column(String(16), nullable=False)
	password = Column(String(60), nullable=False) # bcrypt 최대 60자
	created_at = Column(DateTime, nullable=False, default=datetime.now)
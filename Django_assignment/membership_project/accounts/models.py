from django.db import models
from common.models import CommonModel
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(CommonModel, AbstractUser):
	phone_number = models.CharField(max_length=15, blank=True, null=True)

	def __str__(self):
		return self.username

	class Meta:
		verbose_name_plural = "Users" # 모델 목록 이름 변경
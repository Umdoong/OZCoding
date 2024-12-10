from django.db import models
from common.models import CommonModel

# Create your models here.
class AddressesModel(CommonModel):
	user = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
	street = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	country = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "Addresses" # 모델 목록 이름 변경
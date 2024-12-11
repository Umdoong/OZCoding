from rest_framework.serializers import ModelSerializer
from .models import AddressesModel

class AddressSerializer(ModelSerializer):

	class Meta:
		model = AddressesModel
		fields = ['id', 'user', 'street', 'city', 'state', 'postal_code', 'country']
		depth = 1
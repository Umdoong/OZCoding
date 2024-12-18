from .models import AddressesModel
from accounts.models import Account
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class AddressAPITestCase(APITestCase):
	def setUp(self):
		self.user = Account.objects.create_user(username='tester', password='password')
		self.address = AddressesModel.objects.create(user=self.user, street='98', city='원주', state='강원도', postal_code='12345', country='대한민국')
		refresh = RefreshToken.for_user(self.user)
		self.token = str(refresh.access_token)
		self. client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

	def test_get_addresses_unauthorized(self):
		self.client.logout()
		# 특정 url로 요청을 보내기 위해 reverse 사용
		url = reverse('addresses_list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_get_addresses(self):
		self.client.login(username='tester', password='password')
		url = reverse('addresses_list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)

	def test_create_address(self):
		self.client.login(username='tester', password='password')

		url = reverse('create_user_address', kwargs={'user_id': self.user.id})
		data = {
			'street': "99",
			'city': "강남구",
			'state': "서울시",
			'postal_code': "12346",
			'country': "대한민국"
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_address(self):
		self.client.login(username='tester', password='password')
		url = reverse('update_address', kwargs={'pk': self.address.pk})
		data = {
			'street': "동해",
		}
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.address.refresh_from_db()
		self.assertEqual(self.address.street, "동해")

	def test_delete_address(self):
		url = reverse('delete_address', kwargs={'pk': self.address.pk})
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(AddressesModel.objects.filter(pk=self.address.pk).exists())
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path("", views.AddressesList.as_view()),
	path("<int:pk>/", views.AddressDetail.as_view(), name='address_detail'),
	path("<int:user_id>/add", views.CreateUserAddress.as_view(), name='create_user_address'),
	path("<int:pk>/update", views.UpdateAddress.as_view(), name='update_address'),
	path("<int:pk>/delete", views.DeleteAddress.as_view(), name='delete_address'),
	path("getToken", obtain_auth_token),
]
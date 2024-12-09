from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class AccountAdmin(UserAdmin):
	model = User
	list_display = ('username', 'email', 'phone_number', 'create_at', 'updated_at')
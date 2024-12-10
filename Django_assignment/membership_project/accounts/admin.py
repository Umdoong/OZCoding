from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(UserAdmin):
	list_display = ('username', 'email', 'phone_number', 'create_at', 'updated_at')

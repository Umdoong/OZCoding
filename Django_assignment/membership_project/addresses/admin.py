from django.contrib import admin
from .models import AddressesModel
# Register your models here.
@admin.register(AddressesModel)
class AddressesModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'street', 'city', 'state', 'postal_code', 'country')
	list_filter = ('city', 'state', 'country')
	search_fields = ('user__username', 'street', 'postal_code', 'city', 'state')
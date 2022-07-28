from django.contrib import admin
from apps.purchase.models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'vehicle', 'cost']
    search_fields = ['vehicle']
    list_filter = ['buyer', 'vehicle', 'cost']


admin.site.register(Purchase, PurchaseAdmin)

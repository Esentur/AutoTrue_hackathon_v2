from django.contrib import admin

from apps.account.models import MyUser
from apps.purchase.models import Purchase


class PurchaseInAdmin(admin.TabularInline):
    model = Purchase
    fields = ['buyer']

class MyUserAdmin(admin.ModelAdmin):
    inlines = [PurchaseInAdmin]
    list_display = ['username', 'email']



admin.site.register(MyUser, MyUserAdmin)

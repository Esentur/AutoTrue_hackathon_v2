from django.contrib import admin

from apps.account.models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']



admin.site.register(MyUser, MyUserAdmin)

from django.contrib import admin

from apps.account.models import MyUser

# class MyUserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email', 'created_at']
#     list_filter = ['category']
#     search_fields = ['id']

admin.site.register(MyUser)
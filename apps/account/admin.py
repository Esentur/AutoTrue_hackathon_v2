from django.contrib import admin

from apps.account.models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'image_tag']
    readonly_fields = ['image_tag']
    def image_tag(self, obj):
        return f'<img src={obj.avatar.url}'

    image_tag.short_description = 'avatar'
    image_tag.allow_tags = True


admin.site.register(MyUser, MyUserAdmin)

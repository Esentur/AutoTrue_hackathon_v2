from django.contrib import admin

from apps.vehicle.models import Vehicle, Image, Type


class ImangeInProduct(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 5
    extra = 0


class ImageAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'image']
    search_fields = ['vehicle']
    list_filter = ['vehicle']

class TypeAdmin(admin.ModelAdmin):
    search_fields = ['slug']

class VehicleAdmin(admin.ModelAdmin):
    inlines = [ImangeInProduct]
    list_display = ['title','seller', 'price']
    search_fields = ['title']
    list_filter = ['title','year','price']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Type,TypeAdmin)

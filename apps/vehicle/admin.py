from django.contrib import admin

from apps.vehicle.models import Vehicle, Image, Type, Review, Like


class ImageInProduct(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 5
    extra = 0


class ReviewInAdmin(admin.TabularInline):
    model = Review
    extra = 0


class ImageAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'image']
    search_fields = ['vehicle']
    list_filter = ['vehicle']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at']
    search_fields = ['text']
    list_filter = ['author']


class TypeAdmin(admin.ModelAdmin):
    search_fields = ['slug']


class VehicleAdmin(admin.ModelAdmin):
    inlines = [ImageInProduct, ReviewInAdmin]
    list_display = ['id', 'title', 'seller', 'price']
    search_fields = ['id','title']
    list_filter = ['title', 'year', 'price']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Like)

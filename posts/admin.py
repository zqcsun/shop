from django.contrib import admin
from .models import Post, Car, Detail

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'active')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('active', 'created',)
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'driver', 'post')
    search_fields = ('make', 'model')
    list_filter = ('year',)
@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('car', 'key', 'value')
    search_fields = ('key', 'value')
    
# Register your models here.
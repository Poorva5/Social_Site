from django.contrib import admin
from .models import UserData, PostData

admin.site.register(UserData)


@admin.register(PostData)
class PostDataAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created_at']
    list_filter = ['created_at']


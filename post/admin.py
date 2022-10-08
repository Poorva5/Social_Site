from django.contrib import admin
from .models import PostData

@admin.register(PostData)
class PostDataAdmin(admin.ModelAdmin):
    list_display = ['caption','image', 'created_at']
    list_filter = ['created_at']
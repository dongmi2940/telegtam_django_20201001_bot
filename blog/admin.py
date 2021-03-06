from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'update_at'] 
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
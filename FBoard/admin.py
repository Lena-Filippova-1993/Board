from django.contrib import admin

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'dateCreation']
    list_filter = ('author', 'dateCreation')

admin.site.register(Post, PostAdmin)
admin.site.register(Response)

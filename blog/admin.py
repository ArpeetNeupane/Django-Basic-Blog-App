from django.contrib import admin
from .models import Post, Comment, Like

#we register our models(eg = post) here so that they show up in the admin page

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

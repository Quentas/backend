from django.contrib import admin
from .models import Account, Post, Comment


admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Comment)

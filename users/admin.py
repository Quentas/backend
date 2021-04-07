from django.contrib import admin
from .models import (
    Account,
    Post,
    Comment,
    Picture,
)


admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Picture)

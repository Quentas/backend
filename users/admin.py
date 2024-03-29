from django.contrib import admin
from rest_framework_simplejwt import token_blacklist

from .models import (
    Account,
    Post,
    Comment,
    Picture,
)


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True 

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)


admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Picture)



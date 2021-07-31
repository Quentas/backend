from django_filters import rest_framework as filters
from .models import Post, Account
from django.contrib.contenttypes.models import ContentType


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class PostFilter(filters.FilterSet):
    user = CharFilterInFilter(field_name="username", lookup_expr="iexact")

    class Meta:
        model = Post
        fields = ['user']


def modify_input_for_multiple_files(property_id, image):
    dict = {}
    dict['property_id'] = property_id
    dict['image'] = image
    return dict


def is_fan(obj, user) -> bool:
    """
    Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    return obj.likes.filter(username=user).exists()

def get_fans(obj):
    """
    Получает всех пользователей, которые лайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return Account.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)



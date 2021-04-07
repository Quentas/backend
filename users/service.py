from django_filters import rest_framework as filters
from .models import Post


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
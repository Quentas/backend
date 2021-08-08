from django_filters import rest_framework as filters
from .models import Post, Account, Picture
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from pathlib import Path

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

def is_booked(obj, user) -> bool:
    """
    Проверяет, репостнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    return obj.bookmark.filter(username=user).exists()


def get_fans(obj):
    """
    Получает всех пользователей, которые лайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return Account.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)


def validate_images(images):
    if len(images) > 6: 
        return Response({"Image upload error": "Too many images uploaded. Maximum amount is 6"}, status=400)
    for image in images:  ##  fistly check all images
        print(image)
        print(image.size, end='\n')
        if image.size > 2000000:  ## 2 MB
            return Response({"Image upload error": "Too big images uploaded. Maximum size is 2 MB"}, status=400)
        if not Path(str(image)).suffix in {'.jpg', '.jpeg', '.png'}:
            return Response({"Image upload error": "Images of formats jpg, jpeg, png are supported"}, status=400)
    return True

def is_stored_on_server(image):
    try:
        return image.startswith('http://127.0.0.1:8000/media/pictures/') or image.startswith('https://fierce-dusk-92502.herokuapp.com/media/pictures/')
    except:
        return False
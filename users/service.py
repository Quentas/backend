from pathlib import Path
import random
import string

from django.http import JsonResponse
from django_filters import rest_framework as filters
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response

from .models import Account


def is_fan(obj, user) -> bool:
    """
    Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    return obj.likes.filter(username=user).exists()


def is_subscribed(obj, user) -> bool:
    """
    Проверяет, подписан ли `user` на `obj`.
    """
    if not user.is_authenticated:
        return False
    return user.subscribed_to.filter(username=obj).exists()


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
        return Response({"detail": "Too many images uploaded. Maximum amount is 6"}, status=400)
    for image in images:
        if image.size > 2000000:  ## 2 MB
            return Response({"detail": "Too big images uploaded. Maximum size is 2 MB"}, status=400)
        if not Path(str(image)).suffix in {'.jpg', '.jpeg', '.png', '.gif'}:
            return Response({"detail": "Images of formats jpg, jpeg, png are supported"}, status=400)
    return True


def password_generate(length):
    all = string.ascii_letters + string.digits
    password = "".join(random.sample(all, length))
    return password

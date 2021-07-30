from rest_framework.decorators import action
from rest_framework.response import Response
from . import service


class LikedMixin:
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        """
        Лайкает `obj`.
        """
        obj = self.get_object()
        service.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        """
        Удаляет лайк с `obj`.
        """
        obj = self.get_object()
        service.remove_like(obj, request.user)
        return Response()

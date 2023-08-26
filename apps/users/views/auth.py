from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import UserProfile
from users.serializers import UserProfileSerializer


class ProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    http_method_names = ('get', 'patch', 'delete')

    def get_object(self):
        user = self.request.user
        if user.is_authenticated and user.username == self.kwargs['username']:
            return user
        user = UserProfile.objects.filter(username=self.kwargs['username'])
        if user:
            return user.first()
        raise Http404

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user != self.get_object():
                raise PermissionDenied()
            self.perform_destroy(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise NotAuthenticated()

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user != self.get_object():
                raise PermissionDenied()
            partial = kwargs.pop('partial', False)
            instance = request.user
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        raise NotAuthenticated()

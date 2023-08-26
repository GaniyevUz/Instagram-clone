from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.permissions import IsPublicAccount
from users.models import UserProfile
from users.serializers import UserProfileSerializer, UserFollowingModelSerializer, UserFollowModelSerializer
from users.serializers.users import UserViewProfileModelSerializer


class UserProfileModelViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser]


class FollowListCreateAPIVIew(ListCreateAPIView):
    serializer_class = UserFollowingModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.following.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserViewProfileModelSerializer(page, many=True, context={'request': self.request})
            return self.get_paginated_response(serializer.data)

        serializer = UserViewProfileModelSerializer(queryset, many=True, context={'request': self.request})
        return Response(serializer.data)


class UnFollowAPIView(DestroyAPIView):
    queryset = UserProfile.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.following.filter(id=instance.id).first():
            user.following.remove(instance)
            instance.followers.remove(user)
            instance.save()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404


class FollowersListAPIVIew(ListAPIView):
    serializer_class = UserViewProfileModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers.all()


class FollowersListAPIViewByUsername(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserViewProfileModelSerializer
    permission_classes = (IsPublicAccount,)

    def get_queryset(self):
        if username := self.kwargs.get('username'):
            qs = super().get_queryset().filter(username=username)
            if qs.exists():
                user: UserProfile = qs.first()
                return user.followers.all()
        raise Http404


class FollowingListAPIViewByUsername(FollowersListAPIViewByUsername):
    def get_queryset(self):
        if username := self.kwargs.get('username'):
            qs = self.queryset.filter(username=username)
            if qs.exists():
                user: UserProfile = qs.first()
                return user.following.all()
        raise Http404

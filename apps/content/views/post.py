from uuid import uuid4

from django.utils.decorators import method_decorator
from drf_yasg import openapi, utils
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from content.models import Post
from content.serializers import PostModelSerializer, UpdatePostModelSerializer


@method_decorator(name='create', decorator=utils.swagger_auto_schema(manual_parameters=[openapi.Parameter(
    name='media',
    in_=openapi.IN_FORM,
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=True,
    description='media'
)]))
class PostModelViewSet(ModelViewSet):
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdatePostModelSerializer
        return super().get_serializer_class()

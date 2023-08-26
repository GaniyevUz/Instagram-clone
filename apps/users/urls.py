from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from users.views import UserProfileModelViewSet, ProfileRetrieveUpdateDestroyAPIView, \
    FollowListCreateAPIVIew, FollowersListAPIVIew, FollowersListAPIViewByUsername, FollowingListAPIViewByUsername, \
    UnFollowAPIView

urlpatterns = [
    path('following', FollowListCreateAPIVIew.as_view()),
    path('following/<str:username>', FollowingListAPIViewByUsername.as_view()),
    path('unfollow/<str:username>', UnFollowAPIView.as_view()),
    path('followers', FollowersListAPIVIew.as_view()),
    path('followers/<str:username>', FollowersListAPIViewByUsername.as_view()),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('<str:username>', ProfileRetrieveUpdateDestroyAPIView.as_view()),
]

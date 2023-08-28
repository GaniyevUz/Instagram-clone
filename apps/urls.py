from django.urls import path, include

urlpatterns = [
    path('user/', include('users.urls')),
    path('', include('content.urls')),
    path('chat/', include('chat.urls')),
]

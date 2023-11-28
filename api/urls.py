from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.TestViewset import TestViewset
from api.views.AuthViewset import LoginView, RegisterView, ProfileView
from api.views.ChatViewset import ChatViewSet

router = SimpleRouter()
router.register('test', TestViewset, basename='test')
router.register('chats', ChatViewSet, basename='chats')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
]

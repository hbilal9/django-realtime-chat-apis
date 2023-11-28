from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.TestViewset import TestViewset
from api.views.AuthViewset import LoginView

router = SimpleRouter()
router.register('test', TestViewset, basename='test')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

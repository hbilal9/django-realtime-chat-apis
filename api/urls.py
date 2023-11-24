from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views.TestViewset import TestViewset

router = SimpleRouter()
router.register('test', TestViewset, basename='test')

urlpatterns = [
    path('', include(router.urls)),
]

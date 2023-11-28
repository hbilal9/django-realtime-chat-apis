from django.urls import path
from .consumers.TestConsumer import TestConsumer
from .consumers.ThreadConsumer import ThreadConsumer

websocket_urlpatterns = [
    path('ws/test/<str:username>/', TestConsumer.as_asgi()),
    path('ws/thread/<str:username>/', ThreadConsumer.as_asgi()),
]
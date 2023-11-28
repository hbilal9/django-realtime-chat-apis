from django.urls import path
from .consumers.TestConsumer import TestConsumer

websocket_urlpatterns = [
    path('ws/test/<str:username>/', TestConsumer.as_asgi()),
    path('ws/chat/', TestConsumer.as_asgi()),
]
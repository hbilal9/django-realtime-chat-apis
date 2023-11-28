from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.models import Thread, Message
from api.serializers.chatSerializer import ThreadSerializer, MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(first_person=user) | Thread.objects.filter(second_person=user)
    
    @action(detail=True, methods=['get'], url_path='messages')
    def messages(self, request, pk=None):
        thread = self.get_object()
        messages = Message.objects.filter(thread=thread)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
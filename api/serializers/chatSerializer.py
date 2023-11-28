from rest_framework import serializers
from api.models import Thread, Message

class ThreadSerializer(serializers.ModelSerializer):
    first_person = serializers.SerializerMethodField()
    second_person = serializers.SerializerMethodField()
    class Meta:
        model = Thread
        fields = ('id', 'first_person', 'second_person', 'created_at', 'updated_at')

    def get_first_person(self, obj):
        return {
            'id': obj.first_person.id,
            'username': obj.first_person.username,
            'full_name': obj.first_person.fullName()
        } if obj.first_person.id != self.context['request'].user.id else obj.first_person.id
    
    def get_second_person(self, obj):
        return {
            'id': obj.second_person.id,
            'username': obj.second_person.username,
            'full_name': obj.second_person.fullName(),
        } if obj.second_person.id != self.context['request'].user.id else obj.second_person.id
class MessageSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ('id', 'thread', 'sender', 'text', 'created_at', 'updated_at')
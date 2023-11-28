from channels.generic.websocket import AsyncWebsocketConsumer
from api.serializers.chatSerializer import MessageSerializer
from api.models import Thread, Message, User
from channels.db import database_sync_to_async
import json
from datetime import datetime

class ThreadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f"thread_{self.username}"
        user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.update_user_remarks(self.username, "online")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # user = await self.get_user_object(self.username)
        # print("Thread: disconnect", user.first_name, user.last_name)
        await self.update_user_last_seen(self.username)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print("Thread: receive", text_data_json)

        # await self.create_message(text_data_json['data'])
        # serializer = MessageSerializer(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'sender_id': text_data_json['data']['send_from'],
                'thread_id': text_data_json['data']['thread_id'],
                'text': text_data_json['data']['text'],
            }
        )

        thread = await self.get_thread_object(text_data_json['data']['thread_id'])
        reciever_user_id = thread.first_person_id if thread.first_person_id != text_data_json['data']['send_from'] else thread.second_person_id

        receiver_user = await self.get_user_object(int(reciever_user_id))
        receiver_room_group_name = f"thread_{receiver_user.username}"
        await self.channel_layer.group_send(
            receiver_room_group_name,
            {
                'type': 'send_message',
                'sender_id': text_data_json['data']['send_from'],
                'thread_id': text_data_json['data']['thread_id'],
                'text': text_data_json['data']['text'],
            }
        )

    async def send_message(self, event):
        print("thread: send_message", event)
        await self.send(text_data=json.dumps({
            'send_from': event['sender_id'],
            'thread_id': event['thread_id'],
            'text': event['text'],
        }))

    @database_sync_to_async
    def create_message(self, data):
        message = Message.objects.create(
            thread_id=data['thread_id'],
            sender_id=data['send_from'],
            text=data['text']
        )
        return message
    
    @database_sync_to_async
    def get_user_object(self, id):
        if type(id) == str:
            return User.objects.get(username=id) or None
        else:
            return User.objects.get(pk=id) or None
    
    @database_sync_to_async
    def get_thread_object(self, id):
        return Thread.objects.get(pk=id) or None
    
    @database_sync_to_async
    def update_user_last_seen(self, username):
        user = User.objects.get(username=username)
        user.last_login = datetime.now()
        user.remarks = ""
        user.save()
        return user
    
    @database_sync_to_async
    def update_user_remarks(self, username, remarks):
        user = User.objects.get(username=username)
        user.remarks = remarks
        user.save()
        return user
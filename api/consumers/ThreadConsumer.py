from channels.generic.websocket import AsyncWebsocketConsumer
from api.serializers.chatSerializer import MessageSerializer, ThreadUserSerializer
from api.models import Thread, Message, User
from channels.db import database_sync_to_async
import json
from datetime import datetime
from django.http.request import HttpRequest

class ThreadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f"thread_{self.username}"
        user = self.scope['user']
        print(datetime.now())
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.update_user_remarks(self.username, "online")
        await self.user_status(self.username)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # user = await self.get_user_object(self.username)
        # print("Thread: disconnect", user.first_name, user.last_name)
        user = await self.update_user_last_seen(self.username)
        await self.user_status(self.username)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print("Thread: receive", text_data_json)

        await self.create_message(text_data_json['data'])
        # serializer = MessageSerializer(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_online_status',
            }
        )

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
            'type': 'new_message',
            'send_from': event['sender_id'],
            'thread_id': event['thread_id'],
            'text': event['text'],
        }))

    async def send_online_status(self, event):
        print("thread: send_online_status", event)
        await self.send(text_data=json.dumps(event))

    async def user_status(self, username):
        threads = await self.get_user_threads(username)
        for thread in threads:
            if thread['first_person']['username'] == username:
                await self.channel_layer.group_send(
                    f"thread_{thread['second_person']['username']}",
                    {
                        'type': 'send_online_status',
                        'thread_id': thread['id'],
                        'first_person': {
                            'id': thread['first_person']['id'],
                            'username': thread['first_person']['username'],
                            'avatar': thread['first_person']['avatar'],
                            'full_name': thread['first_person']['full_name'],
                            'last_seen': thread['second_person']['last_seen'].strftime('%Y-%m-%d %H:%M:%S'),
                            'active_status': thread['first_person']['active_status'],
                        },
                        'second_person': thread['second_person']['id'],
                        # 'created_at': thread['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                        # 'updated_at': thread['updated_at'].strftime('%Y-%m-%d %H:%M:%S'),
                    }
                )
            else:
                await self.channel_layer.group_send(
                    f"thread_{thread['first_person']['username']}",
                    {
                        'type': 'send_online_status',
                        'id': thread['id'],
                        'first_person': thread['second_person']['id'],
                        'second_person': {
                            'id': thread['second_person']['id'],
                            'username': thread['second_person']['username'],
                            'avatar': thread['second_person']['avatar'],
                            'full_name': thread['second_person']['full_name'],
                            'last_seen': thread['second_person']['last_seen'].strftime('%Y-%m-%d %H:%M:%S'),
                            'active_status': thread['second_person']['active_status'],
                        },
                        # 'created_at': thread['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                        # 'updated_at': thread['updated_at'].strftime('%Y-%m-%d %H:%M:%S'),
                    }
                )

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
    
    @database_sync_to_async
    def get_user_threads(self, username):
        user = User.objects.get(username=username)
        threads = Thread.objects.filter(first_person=user) | Thread.objects.filter(second_person=user)
        request = HttpRequest()
        request.user = user
        serializer = ThreadUserSerializer(threads, many=True, context={'request': request})
        return serializer.data
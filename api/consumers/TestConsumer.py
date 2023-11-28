from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f"ticket_assign_{self.username}"
        user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(user.username, "connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("TicketAssignConsumer: receive", text_data_json)
        await self.send(text_data=json.dumps({
            'send_from': text_data_json['data']['send_from'],
            'thread_id': text_data_json['data']['thread_id'],
            'text': text_data_json['data']['text'],
        }))

    async def send_message(self, event):
        print("TicketAssignConsumer: send_message", event)
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'data': event['data']
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test'  # You can make this dynamic if needed
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send a connection established message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected!'
        }))

    async def receive(self, text_data):
        # Parse the incoming message
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Send the received message to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

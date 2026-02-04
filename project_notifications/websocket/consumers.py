import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.user_id = None
        self.notification_group = None

    async def connect(self):
        self.user = self.scope.get('user')

        if not self.user:
            await self.close(code=4008)
            return

        self.user_id = str(self.user.user_id).lower().strip()
        self.notification_group = f"user_{self.user_id}_notifications"
        await self.channel_layer.group_add(self.notification_group, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection.established',
            'user_id': str(self.user.user_id)
        }))

    async def disconnect(self, close_code):
        if self.notification_group:
            await self.channel_layer.group_discard(self.notification_group, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': 'Invalid JSON'
            }))
            return

        action = data.get('action')
        request_id = data.get('request_id', '')

        if action == 'ping':
            await self.send(text_data=json.dumps({
                'type': 'pong',
                'request_id': request_id
            }))

    async def notification_sent(self, event):
        await self.send(text_data=json.dumps(event['data']))

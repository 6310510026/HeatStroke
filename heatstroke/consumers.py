import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # รับ group_id จาก URL
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"group_{self.group_id}"

        # เข้าร่วมกลุ่ม
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # ยืนยันการเชื่อมต่อ
        await self.accept()

    async def disconnect(self, close_code):
        # ออกจากกลุ่ม
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # รับข้อความจาก WebSocket
    async def receive(self, text_data):
        # ข้อความที่รับจาก client (ในกรณีนี้สามารถรับข้อความของข้อมูลที่ต้องการ)
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # ส่งข้อมูลไปยังกลุ่ม
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_update',
                'message': message
            }
        )

    # ส่งข้อมูลไปยัง WebSocket
    async def group_update(self, event):
        message = event['message']

        # ส่งข้อความไปยัง WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

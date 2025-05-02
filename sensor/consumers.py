# sensor/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # ตรงนี้คือการเชื่อมต่อกับ WebSocket
        self.room_group_name = "sensor_group"
        # เริ่มต้นการเชื่อมต่อ WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # เมื่อการเชื่อมต่อถูกตัด
        pass

    async def receive(self, text_data):
        # รับข้อมูลที่ส่งมาจาก WebSocket
        data = json.loads(text_data)
        # ส่งข้อมูลกลับไปยัง WebSocket
        await self.send(text_data=json.dumps(data))

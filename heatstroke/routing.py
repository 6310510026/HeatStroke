# routing.py ในแอปที่คุณใช้ WebSocket
from django.urls import re_path
from . import consumers

# กำหนด routing สำหรับ WebSocket
websocket_urlpatterns = [
    re_path(r'ws/sensor/$', consumers.SensorConsumer.as_asgi()),
]

"""
ASGI config for heatstroke project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# your_project/asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers  # ปรับชื่อให้ตรงกับแอปของคุณ

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heatstroke.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                # เส้นทาง WebSocket สำหรับการเชื่อมต่อข้อมูล real-time ใน group
                path('ws/group/<int:group_id>/', consumers.GroupConsumer.as_asgi()),
            ]
        )
    ),
})



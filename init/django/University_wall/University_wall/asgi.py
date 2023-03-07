"""
ASGI config for University_wall project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from University_wall import routing
from channels.routing import ProtocolTypeRouter,URLRouter




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'University_wall.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({

    "http":get_asgi_application(),#自动找urLs.py, 找视图函数
    "websocket":URLRouter(routing.websocket_urlpatterns),# routings(urLs) 、consumers (views)

})

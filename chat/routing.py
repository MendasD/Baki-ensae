from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('', consumers.JoinAndLeave.as_asgi()),
    path('Messagerie/groups/<uuid:uuid>/', consumers.GroupConsumer.as_asgi()),
]
#re_path(r'ws/Messagerie/groups/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
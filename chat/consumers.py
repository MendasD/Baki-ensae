from django.contrib.auth.models import User
from .models import Event, Message, Group
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from asgiref.sync import sync_to_async
from channels.layers import channel_layers # type: ignore
from channels.db import database_sync_to_async 
import asyncio
import json

# JoinAndLeave Consumer

class JoinAndLeave(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"] # le scope contient toutes les informations sur la connexion, y compris le user authentifié
        await self.accept() # on attend que la connexion au websocket soit établie

    async def receive(self, text_data=None, bytes_data=None):

        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        if type:
            data = text_data.get("data", None)
            
            if type == "leave_group":
                await self.leave_group(data)
            elif type == "join_group":
                await self.join_group(data)

    @sync_to_async
    def get_group(self, group_uuid):
        return Group.objects.get(uuid=group_uuid)

    @sync_to_async
    def remove_user_from_group(self, group):
        group.remove_user_from_group(self.user)

    @sync_to_async
    def add_user_to_group(self, group):
        group.add_user_to_group(self.user)

    async def leave_group(self, group_uuid):
        group = await self.get_group(group_uuid)
        await self.remove_user_from_group(group)
        data = {
            "type": "leave_group",
            "data": group_uuid
        }
        await self.send(text_data=json.dumps(data))

    async def join_group(self, group_uuid):
        group = await self.get_group(group_uuid)
        await self.add_user_to_group(group)
        data = {
            "type": "join_group",
            "data": group_uuid
        }
        await self.send(text_data=json.dumps(data))
    async def disconnect(self, code):
        pass



# GroupeConsumer

class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.group = await database_sync_to_async(Group.objects.get)(uuid = self.group_uuid)
        await self.channel_layer.group_add(# Ajouter un groupe (une instance de GroupConsumer) à un canal (channel_layer)
                self.group_uuid,self.channel_name)
   
        self.user = self.scope["user"]
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        message = text_data.get("message", None)
        author = text_data.get("author", None)
        reponse_id = text_data.get("reponse_id", None)

        print(f"Received data: {text_data}")

        # On vérifie si reponse_id est None ou si le message de réponse n'existe pas
        if reponse_id:
            try:
                reponse = await database_sync_to_async(Message.objects.get)(id=reponse_id)
            except Message.DoesNotExist:
                reponse = None
        else:
            reponse = None

        if type == "text_message":
            user = await database_sync_to_async(User.objects.get)(username=author)
            message= await database_sync_to_async(Message.objects.create)(
            author = user,
            content = message,
            group =self.group,
            response = reponse
            )

            print(f"Created message: {message}")

        # Préparation les données pour l'envoi (NB: sans la synchronisation avec la base, il y aura un probleme)
        response_author = ""
        response_content = ""
        if reponse:
            response_author = await database_sync_to_async(lambda: reponse.author.username)()
            response_content = await database_sync_to_async(lambda: str(reponse.content))()


        await self.channel_layer.group_send(self.group_uuid, {
            "type":"text_message",
            "message_id": message.id,
            "message":str(message),
            "content":str(message.content),
            "heure": message.timestamp.strftime("%H:%M"),  # formatage de l'heure
            "author":author,
            "reponse_author": response_author,
            "reponse_content": response_content
            
        })
        print(f"Sent message to group: {self.group_uuid}")

    async def text_message(self, event):
        print(f"Received event: {event}")
        message = event["message"]
        message_id = event.get("message_id")
        author = event.get("author")
        content = event.get("content")
        heure = event.get("heure")
        reponse_author = event.get("reponse_author")
        reponse_content = event.get("reponse_content")

        returned_data = {
            "type":"text_message",
            "message":message,
            "content":content,
            "heure":heure,
            "group_uuid":self.group_uuid,
            "author":author,
            "message_id":message_id,
            "reponse_author": reponse_author,
            "reponse_content": reponse_content
        }
        await self.send(json.dumps(
                returned_data
                ))
        print(f"Sent data to WebSocket: {returned_data}")
    async def event_message(self, event):
        message = event.get("message")
        user = event.get("user", None)
        
        await self.send(
            json.dumps(#convertit un objet python en une chaîne JSON
                        {
                    "type":"event_message",
                    "message":message,
                    "status":event.get("status",None),
                    "user":user
                        }
                    )
            )
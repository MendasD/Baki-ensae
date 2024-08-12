from django.dispatch import receiver
from .models import Event
from django.db.models.signals import post_save
from channels.layers import get_channel_layer # type: ignore
from asgiref.sync import async_to_sync

# Pour envoyer les évènements (join, leave) au niveau du frontend

@receiver(post_save, sender=Event)#ce decorateur lie cette fonction a l'evenement post_save du model Event et est appelé chaque fois qu'un évènement est sauvegardé
def broadcast_event_to_groups(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_uuid = str(instance.group.uuid)
    event_message = str(instance)
    async_to_sync(channel_layer.group_send)(group_uuid,
        {
        "type":"event_message",# le broadcast sera reçu dans la methode 'event_message' du consumer
        "message":event_message,
        "status":instance.type,
        "user":str(instance.user)
        }
)
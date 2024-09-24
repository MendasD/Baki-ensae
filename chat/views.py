from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def HomeView(request):
   '''The homepage where all groups are listed '''
   groups = Group.objects.all()
   user = request.user
   context = {
       "groups":groups,
       "user":user
   }
   return render(request,template_name="chat/home2.html",context=context)

@login_required
def GroupChatView(request, uuid):
   '''The view for a group where all messages and events are sent to the frontend'''

   group = get_object_or_404(Group, uuid=uuid)
   if request.user not in group.members.all():
       return HttpResponseForbidden("Vous n'êtes pas un membre de ce groupe.\
                                       Vous pouvez le joindre en utilisant le bouton join")
  
   messages = group.message_set.filter(visible=True)
   
   '''
   messages are the message the members
   of a group send to the group
   '''

   events = group.event_set.all()
   '''
   events are the messages that indicates
   that a user joined or left the group.
   They will be sent automatically when a user join or leave the group
   '''


   #Combine the events and messages for a group
   message_and_event_list = [*messages, *events]

   # Sort the combination by the timestamp so that they are listed in order
   sorted_message_event_list = sorted(message_and_event_list, key=lambda x : x.timestamp)

   #get the list of all group members
   group_members = group.members.all()

   context ={
       "message_and_event_list":sorted_message_event_list,
       "group_members":group_members,
       }

   return render(request, template_name="chat/groupchat.html", context=context)

@csrf_exempt
def supprimer_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            message_id = data.get('message_id',"")
            try:
                message = Message.objects.get(id=message_id)
                message.visible = False
                message.save()
                #message.delete()
                return JsonResponse({'status': 'success'})
            except Message.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)
        except Exception as e:
            print('probleme')
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

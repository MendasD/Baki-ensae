from django.urls import path, include
from . import views

urlpatterns = [
   path("", views.HomeView, name="home"),
   path("groups/<uuid:uuid>/", views.GroupChatView, name="group"),
   path("supprimer_message/", views.supprimer_message, name="supprimer_message")
]
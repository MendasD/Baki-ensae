from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your models here.

class Group(models.Model):
    """
    Group model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Group {self.name}--{self.uuid}"

    def get_absolute_url(self):
        return reverse('groups',args=[str(self.uuid)])
    
    def add_user_to_group(self, user:User): # type: ignore
        self.members.add(user)
        self.event_set.create(type = "Join", user=user)
        self.save()
        
    def remove_user_from_group(self, user:User): # type: ignore
        self.members.remove(user)
        self.event_set.create(type = "Left", user=user)
        self.save()

class Message(models.Model):
    """
    Message model
    """
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey(Group ,on_delete=models.CASCADE)
    response = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.author} : {self.content} @{date} {time.hour}h:{time.minute}min"


class Event(models.Model):
    '''
    A model that holds all events related to a group like when a user joins the group or leaves.
    '''
    CHOICES = [
        ("Join", "join"),
        ("Left", "left")
        ]
    type = models.CharField(choices=CHOICES, max_length=10)
    description= models.CharField(help_text="A description of the event that occurred",\
    max_length=50, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group ,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f"{self.user} {self.type} the {self.group.name} group"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.description}  @{date} at {time.hour}h:{time.minute}min"
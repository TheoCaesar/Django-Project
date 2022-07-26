from enum import auto
from django.db import models

from django.contrib.auth.models import User #we will be linking our profile to users table which is provided
#by django dada. we dont want to alter the users table generated by django, hence we creating the profile

import uuid

from django.db.models.deletion import SET_NULL
from django.db.models.fields import EmailField
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=200, blank = True, null = True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null = True)
    location = models.CharField(max_length=200, blank=True, null = True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null = True)
    profile_image = models.ImageField(null = True, blank = True, upload_to = 'profiles/', default = 'profiles/user-default.png')
    social_github =models.CharField(max_length=200, blank = True, null = True)
    social_twitter =models.CharField(max_length=200, blank = True, null = True)
    social_linkedin =models.CharField(max_length=200, blank = True, null = True)
    social_youtube =models.CharField(max_length=200, blank = True, null = True)
    social_website =models.CharField(max_length=200, blank = True, null = True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key=True, editable = False)

    def __str__(self):      #this renders our objects readable
        return str(self.user.username)
 

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length=200,null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, editable = False, primary_key=True)

    def __str__(self):
        return str(self.name) #someway somehow, dennis decided to add location to the Profile model/table

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True , blank= True)   #on delete is set to null so dt upon deletion of sender's account, the msg remains in database. null is set to true so users sans account can send messages. blank is set to true cos a form can be submitted sans a sender.
    recepient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True , blank= True, related_name='messages')   #on delete is set to null so dt upon deletion of sender's account, the msg remains in database. null is set to true so users sans account can send messages. blank is set to true cos a form can be submitted sans a sender.
    name = models.CharField(max_length=200, null =True, blank=True)
    email = models.EmailField(max_length=200, null =True, blank=True)
    subject = models.CharField(max_length=200, null =True, blank=True)
    body = models.TextField(max_length=200, null =True, blank=True)
    is_read = models.BooleanField(default=False, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, editable = False, primary_key=True)
    

    def __str__(self):
        return self.subject 
    
    class Meta:
        ordering = ['is_read', '-created'] 
        #unread messages will be at the top and if there is more than one it is arranged by date created in descending order

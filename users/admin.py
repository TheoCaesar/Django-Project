from django.contrib import admin

from .models import Profile #added
from .models import Skill #added instead of just appending with a comma above next to Profile
from .models import Message #17 Feb 2022 15:30


# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message) #17 Feb 2022 15:30
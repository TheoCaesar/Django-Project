from django.contrib import admin

# Register your models here.
from .models import ProjecT, review, Tag

admin.site.register(ProjecT)
admin.site.register(review)
admin.site.register(Tag)

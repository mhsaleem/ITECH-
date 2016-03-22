from django.contrib import admin
from models import UserProfile, Title, Pun, Tag

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Title)
admin.site.register(Pun)
admin.site.register(Tag)

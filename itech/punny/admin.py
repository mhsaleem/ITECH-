from django.contrib import admin
from punny.models import UserProfile, Title, Badge, Pun, Tag

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Title)
admin.site.register(Badge)
admin.site.register(Pun)
admin.site.register(Tag)
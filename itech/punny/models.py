from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Title(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    user = models.ManyToManyField(UserProfile)

    def __unicode__(self):
        return self.title


class Badge(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    user = models.ManyToManyField(UserProfile)

    def __unicode__(self):
        return self.title


class Pun(models.Model):
    text = models.CharField(max_length=350)
    owner = models.ForeignKey(UserProfile, related_name='owner')
    score = models.IntegerField(default=0)
    timeStamp = models.DateTimeField(auto_now_add=True)
    flagCount = models.IntegerField(default=0)
    NSFW = models.BooleanField(default=False)

    userVote = models.ManyToManyField(UserProfile, related_name='voted_user')

    def __unicode__(self):
        return self.text


class Tag(models.Model):
    tagText = models.CharField(max_length=28,unique=True)
    pun = models.ManyToManyField(Pun)

    def __unicode__(self):
        return self.tagText
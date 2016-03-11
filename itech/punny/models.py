from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.template.defaultfilters import slugify
# Create your models here.


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, unique=True)
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    # currentBadge = models.OneToOneField(Badge)
    #objects = UserManager()

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Title(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    user = models.ManyToManyField(UserProfile)
    objects = UserManager()

    def __unicode__(self):
        return self.title


class Badge(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    user = models.ManyToManyField(UserProfile)

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    text = models.CharField(max_length=28, unique=True)
    s = models.SlugField()
    def save(self, *args, **kwargs):
        self.s = slugify(self.text)
        super(Tag, self).save(*args, **kwargs)


class Pun(models.Model):
    text = models.CharField(max_length=350)
    owner = models.ForeignKey(User, related_name='owner')
    score = models.IntegerField(default=0)
    timeStamp = models.DateTimeField(auto_now_add=True)
    flagCount = models.IntegerField(default=0)
    NSFW = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    userVote = models.ManyToManyField(UserProfile, related_name='voted_user')

    def __unicode__(self):
        return self.text




    def __unicode__(self):
        return self.text
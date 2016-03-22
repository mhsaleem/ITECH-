import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.template.defaultfilters import slugify
from updown.fields import RatingField
from PIL import Image
from django.db.models.signals import post_save
import titles_per_score
from django.utils import timezone


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, unique=True)
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', default='default-profile.png')
    selected_title = models.ForeignKey('Title')
    # currentBadge = models.OneToOneField(Badge)
    # objects = UserManager()

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
    
    def save(self, *args, **kwargs): #resizes image and crops if not a square, automatically cropping based on the middle

        if not self.id and not self.picture:
            return            

        super(UserProfile, self).save(*args, **kwargs)

        image = Image.open(self.picture)
        (width, height) = image.size

        if image.width > image.height:
            middle = image.width / 2
            distance_from_middle = height/2
            image = image.crop((middle - distance_from_middle, 0, middle + distance_from_middle, image.height))
        else:
            middle = image.height /2
            distance_from_middle = width/2
            image = image.crop((0, middle - distance_from_middle, width, middle + distance_from_middle))

        size = (600, 600)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.picture.path)


def create_profile(sender, instance, created, **kwargs):
    if created:
        title = Title.objects.get_or_create(title="Newb")[0]
        profile, created = UserProfile.objects.get_or_create(user=instance, selected_title=title)
        profile.save()


post_save.connect(create_profile, sender=User)


class Title(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    # user = models.ManyToManyField(UserProfile)
    min_number_days = models.IntegerField(max_length=16, default=0)
    min_score = models.IntegerField(max_length=16, default=0)
    min_number_posts = models.IntegerField(max_length=16, default=0)
    objects = UserManager()

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
    timeStamp = models.DateTimeField(auto_now_add=True)
    flagCount = models.IntegerField(default=0)
    NSFW = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    rating = RatingField(can_change_vote=True)

    def __unicode__(self):
        return self.text

    # def save(self):
    #     for t in titles_per_score.titles:
    #         title = Title.objects.get_or_create(title=t.title)
    #         puns = Pun.objects.filter(owner=self.owner)
    #         total_score = 0
    #         for pun in puns:
    #             pun.score = pun.rating.likes - pun.rating.dislikes
    #             total_score += pun.score
    #         time_elapsed = timezone.now() - self.owner.date_joined
    #         if t.meets_min_score(total_score) & t.meets_account_time(time_elapsed):
    #             title.user.add(self.owner)
    #             title.save()
    #     return



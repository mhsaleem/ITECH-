import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech.settings')

import django

django.setup()

from punny.models import UserProfile, Title, Pun, Tag
from django.contrib.auth.models import User
import datetime


def populate():

    # Create titles to add to users
    add_title(
        title="Grand Punmaster",
        time_in_days=0,
        score=50
    )

    add_title(
        title="Punmonster",
        time_in_days=10,
        score=10,
        posts=10
    )

    add_title(
        title="100 Puns",
        time_in_days=0,
        score=0,
        posts=100
    )
    add_title(
        title="Punter",
        time_in_days=0,
        score=0,
        posts=1
    )

    add_title(
        title="10 Pun Bowling",
        time_in_days=0,
        score=0,
        posts=10
    )

    # Add a tag to be added to puns
    tag_religpun = add_tag(
        text="Religpun",
    )

    tag_name = add_tag(
        text="name",
    )

    tag_jargpun = add_tag(
        text="Jargpun"
    )

    tag_wildlife = add_tag(
        text="wildlife"
    )

    tag_classroom = add_tag(
        text="classroom"
    )

    tag_drugs = add_tag(
        text="drugs"
    )

    tag_law = add_tag(
        text="law"
    )

    ##########################
    # Add a user called rory #
    ##########################
    user_r = add_user(name='rory', password='rory')

    add_user_profile(user_r)

    # Add puns for Rory
    add_pun(
        text="Ro-ro-roryour boat gently down the stream",
        owner=user_r,
        tags=[tag_jargpun, tag_name],
        score=0,
        timestamp=datetime.datetime(2016, 2, 28, 12, 0, 30, 100)
    )

    add_pun(
        text="Whiteboards are remarkable!",
        owner=user_r,
        tags=[tag_classroom],
        score=50,
        timestamp=datetime.datetime(2016, 2, 15, 23, 21, 22, 20)
    )

    ############################
    # Add a user called hashim #
    ############################
    user_h = add_user(name='hashim', password='hashim')

    add_user_profile(user_h)

    add_pun(
        text="I've got some Hashim a pocket",
        owner=user_h,
        tags=[tag_name, tag_drugs],
        score=5,
        nsfw=True,
        timestamp=datetime.datetime(2016, 2, 15, 23, 21, 23, 10)
    )

    ###############################
    # Add a user called alexander #
    ###############################
    user_a = add_user(name='alexander', password='alexander')

    add_user_profile(user_a)

    add_pun(
        text="They're a great couple, Alex-and-her!",
        owner=user_a,
        tags=[tag_name],
        score=1,
        nsfw=True,
        timestamp=datetime.datetime(2016, 2, 10, 8, 8, 8, 8),
    )

    ############################
    # Add a user called leifos #
    ############################
    user_leifos = add_user(name='leifos', password='leifos')

    add_user_profile(user_leifos)

    # Add puns for leifos
    add_pun(
        text="I wish you'd just Leif me alone...",
        owner=user_leifos,
        tags=[tag_wildlife, tag_name],
        score=15,
    )

    add_pun(
        text="My puns are really starting to branch out",
        owner=user_leifos,
        tags=[tag_wildlife],
        score=20
    )

    add_pun(
        text="I've decided to go to back to my hometown to get in touch with my roots",
        owner=user_leifos,
        tags=[tag_wildlife, tag_name],
        score=25
    )

    ###########################
    # Add a user called laura #
    ###########################
    user_laura = add_user(name='laura', password='laura')

    add_user_profile(user_laura)

    # Add puns for user_laura
    add_pun(
        text="I'm just a Laur-unto myself",
        owner=user_leifos,
        tags=[tag_law, tag_name],
        score=15,
    )

    ###########################
    # Add a user called david #
    ###########################
    user_david = add_user(name='david', password='david')

    add_user_profile(user_david)

    # Add puns for user_david
    add_pun(
        text="My friends used to call me David until I lost my ID. Now they just call me Dav",
        owner=user_david,
        tags=[tag_wildlife],
        score=65,
    )


def add_user(name, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.save()
    return u


def add_user_profile(user):
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.save()
    return u


def add_title(title, time_in_days=0, score=0, posts=0):
    t = Title.objects.get_or_create(title=title, min_number_days=time_in_days, min_score=score, min_number_posts=posts)[0]
    t.save()
    return t


def add_pun(text, owner, tags, score, nsfw=False, timestamp=datetime.datetime.now):
    p = Pun.objects.get_or_create(text=text, owner=owner)[0]
    p.rating_likes = score
    p.NSFW = nsfw
    p.timestamp = timestamp
    for tag in tags:
        p.tags.add(tag)
    p.save()
    return p


def add_tag(text):
    t = Tag.objects.get_or_create(text=text)[0]
    t.save()
    return t


# Start execution here!
if __name__ == '__main__':
    print "Starting Punny population script..."
    populate()

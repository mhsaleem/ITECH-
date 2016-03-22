import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech.settings')

import django

django.setup()

from punny.models import UserProfile, Title, Badge, Pun, Tag
from django.contrib.auth.models import User


def populate():
    # Add a user called Rory
    user_r = add_user(name='rory', password='rory')

    add_user_profile(user_r)

    # Create titles to add to users
    add_title(
        title="Grand Punmaster",
        time_in_days=0,
        score=50
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
    tag0 = add_tag(
        text="Religpun",
    )

    # Add puns for user_r
    add_pun(
        text="This is a pun",
        owner=user_r,
        tags=[tag0],
        score=5,
    )

    add_pun(
        text="Whiteboards are remarkable!",
        owner=user_r,
        tags=[tag0],
        score=5,
    )

    add_pun(
        text="Leif me alone....",
        owner=user_r,
        tags=[tag0],
        score=5,
    )

    # Add a user called hashim
    user_h = add_user('hashim', 'hashim')

    add_user_profile(user_h)

    tag0 = add_tag(
        text="Jargpun"
    )
    tag1 = add_tag(
        text="another tag"
    )
    tag2 = add_tag(
        text="pancake day"
    )

    add_title(
        title="Grand Punmonster",
        time_in_days=10,
        score=10,
        posts=10
    )

    add_pun(
        text="This is another pun",
        owner=user_h,
        tags=[tag0, tag2],
        score=5,
    )

    add_pun(
        text="Punday high score",
        owner=user_h,
        tags=[tag0],
        score=20
    )

    add_pun(
        text="Pun to be downvoted",
        owner=user_h,
        tags=[tag0, tag1, tag2],
        score=20
    )

    for t in Title.objects.all(): #TODO: this might need udatd, currently showing all titles rather than just this user
        print "- {0} - {1}".format(str(user_r), str(t))
    for p in Pun.objects.filter(owner=user_r):
        print "- {0} - {1}".format(str(user_r), str(p))
        for t in Tag.objects.filter(pun__tags__pun=p):
            print "- {0}".format('#' + str(t.text) + ", ")


def add_user(name, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.save()
    return u


def add_user_profile(user):
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.picture = 'profile_images/IMG_3483.jpg'
    u.save()
    return u


def add_title(title, time_in_days=0, score=0, posts=0):
    t = Title.objects.get_or_create(title=title, min_number_days=time_in_days, min_score=score, min_number_posts=posts)[0]
    t.save()
    return t


def add_pun(text, owner, tags, score):
    p = Pun.objects.get_or_create(text=text, owner=owner)[0]
    p.rating_likes = score
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
    print "Starting Rango population script..."
    populate()

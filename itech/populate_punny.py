import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech.settings')

import django
django.setup()

from django.contrib.auth.models import User
from punny.models import UserProfile, Title, Badge, Pun, Tag


def populate():

    user_r = add_user(name='Rory')

    user_profile = add_user_profile(user_r)

    add_title(
        title="Grand Punmaster",
        user=user_profile
    )

    add_badge(
        title="100 Puns",
        user=user_profile
    )

    pun = add_pun(
        text="This is a pun",
        owner=user_profile
    )

    add_tag(
        text="Religpun",
        pun=pun
    )

    user_h = add_user('Hashim')

    user_profile = add_user_profile(user_h)

    add_title(
        title="Grand Punmonster",
        user=user_profile
    )

    add_badge(
        title="Infinite Puns",
        user=user_profile
    )

    pun = add_pun(
        text="This is another pun",
        owner=user_profile
    )

    add_tag(
        text="Jargon",
        pun=pun
    )

    for b in Badge.objects.filter(user=user_r):
        print "- {0} - {1}".format(str(user_r), str(b))
    for t in Title.objects.filter(user=user_r):
        print "- {0} - {1}".format(str(user_r), str(t))
    for p in Pun.objects.filter(owner=user_r):
        print "- {0} - {1}".format(str(user_r), str(p))
        for t in Tag.objects.filter(pun=p):
            print "-- {0} - {1}".format(str(p), str(t))


def add_user(name):
    u = User.objects.get_or_create(username=name)[0]
    u.save()
    return u


def add_user_profile(user):
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.save()
    return u


def add_title(title, user):
    t = Title.objects.get_or_create(title=title)[0]
    t.user = user
    t.save()
    return t


def add_badge(title, user):
    b = Badge.objects.get_or_create(title=title)[0]
    b.user = user
    b.save()
    return b


def add_pun(text, owner, score=5):
    p = Pun.objects.get_or_create(text=text, owner=owner)[0]
    p.score=score
    p.save()
    return p


def add_tag(text, pun):
    t = Tag.objects.get_or_create(text=text)[0]
    t.pun = pun
    t.save()
    return t


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
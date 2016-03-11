import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech.settings')

import django
django.setup()

from punny.models import UserProfile, Title, Badge, Pun, Tag
from django.contrib.auth.models import User


def populate():

    user_r = add_user(name='rory', password='rory')

    user_profile = add_user_profile(user_r)

    add_title(
        title="Grand Punmaster",
        user=user_profile
    )

    tag = add_tag(
        text="Religpun",
    )

    add_badge(
        title="100 Puns",
        user=user_profile
    )

    pun = add_pun(
        text="This is a pun",
        owner=user_r,
        tags=[tag]
    )

    pun = add_pun(
        text="Whiteboards are remarkable!",
        owner=user_r,
        tags=[tag]
    )

    pun = add_pun(
        text="Leif me alone....",
        owner=user_r,
        tags=[tag]
    )

    user_h = add_user('hashim', 'hashim')

    user_profile = add_user_profile(user_h)

    tag = add_tag("Jargpun")
    otherTag = add_tag("pancake day")

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
        owner=user_h,
        tags=[tag, otherTag]
    )


    for b in Badge.objects.filter(user=user_r):
        print "- {0} - {1}".format(str(user_r), str(b))
    for t in Title.objects.filter(user=user_r):
        print "- {0} - {1}".format(str(user_r), str(t))
    for p in Pun.objects.filter(owner=user_r):
        print "- {0} - {1}".format(str(user_r), str(p))
        for tag in Tag.objects.filter(pun__tags__pun=p):
            print "- {0}".format('#'+str(tag.text)+", ")
        # for t in Tag.objects.filter(pun=p):
        #     print "-- {0} - {1}".format(str(p), str(t))


def add_user(name, password):
    u = User.objects.get_or_create(username=name, password=password)[0]
    u.save()
    return u


def add_user_profile(user):
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.picture = '/static/images/leonardo-dicaprio.jpg'
    u.save()
    return u


def add_title(title, user):
    t = Title.objects.get_or_create(title=title)[0]
    t.user.add(user)
    t.save()
    return t


def add_badge(title, user):
    b = Badge.objects.get_or_create(title=title)[0]
    b.user.add(user)
    b.save()
    return b


def add_pun(text, owner, tags, score=5):
    p = Pun.objects.get_or_create(text=text, owner=owner)[0]
    p.score = score
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

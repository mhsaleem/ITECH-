import slug as slug
from django.template.defaultfilters import slugify
from watson import search as watson
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from punny.models import Pun, Tag, UserProfile, Badge, Title
import punny_search
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q, Max
from django.contrib.auth.models import User
from forms import PunForm, SearchForm
from datetime import datetime, timedelta
import re
import datetime
import operator


# Reusable function to process a pun submission
def process_pun_form(request):
    form = PunForm(request.POST)
    if form.is_valid():
        # this is working, redirect needs fixed. But currently users do not have profiles automatically
        tags = re.split("; |, ", form.cleaned_data['tags'])
        # converting text to tag objects
        tagObjs = []
        for tag in tags:
            tagObjs.append(Tag.objects.get_or_create(text=tag)[0])

        pun = Pun(text=form.cleaned_data['puntext'],
                  owner=request.user,
                  NSFW=form.cleaned_data['NSFW'],
                  flagCount=0)
        with watson.update_index():
            pun.save()
        for tag in tagObjs:
            pun.tags.add(tag)
            # adding tag objects to the pun
    return form


def setUpDownVotes(request, puns):
    if request.user.is_authenticated():
        if puns != None:
            for pun in puns:
                pun.score = pun.rating.likes - pun.rating.dislikes
                x = pun.rating.get_rating_for_user(request.user)
                if x == 1:
                    pun.upvoted = True
                elif x == -1:
                    pun.downvoted = True
        return puns


def orderQuerySetByPunScore(puns):
    for pun in puns:
        pun.score = pun.rating_likes - pun.rating_dislikes
    puns = sorted(puns, key=operator.attrgetter('score'), reverse=True)
    return puns


def getTopPunInPastDays(days=1):
    now = datetime.datetime.now()
    startDay = now - timedelta(days=days)
    puns = Pun.objects.filter(timeStamp__range=(startDay, now))
    puns = orderQuerySetByPunScore(puns)
    topPun = puns[0]
    return topPun


def index(request):
    user = request.user
    if request.method == 'POST':
        form = process_pun_form(request)
    else:
        form = PunForm()

    context_dict = {'new_pun_form': form}
    context_dict['user'] = user
    context_dict['search_form'] = SearchForm()
    now = datetime.datetime.now()

    context_dict['today'] = getTopPunInPastDays(1)
    context_dict['week'] = getTopPunInPastDays(7)
    context_dict['month'] = getTopPunInPastDays(30)
    return render(request, 'punny/index.html', context_dict)


def search(request):
    if request.method == 'POST':
        form = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'new_pun_form': form, 'search_form': SearchForm()}
    query_string = ""
    puns = None

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        data = search_form.cleaned_data
        query_string = data['search']
        puns = watson.filter(Pun, query_string)

    puns = setUpDownVotes(request, puns)
    puns = orderQuerySetByPunScore(puns)
    context_dict['query_string'] = query_string
    context_dict['puns'] = puns

    return render_to_response('punny/search-results.html',
                              context_dict,
                              context_instance=RequestContext(request))

    # return render(request, 'punny/search-results.html', context_dict)


def tag_detail(request, tag_name_slug):
    if request.method == 'POST':
        form = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'new_pun_form': form, 'search_form': SearchForm()}
    try:
        tag_name_slug = slugify(tag_name_slug)
        tag = Tag.objects.get(s=tag_name_slug)
        puns = Pun.objects.filter(Q(tags__text__exact=tag.text))
        for pun in puns:
            pun.score = pun.rating_likes - pun.rating_dislikes
        puns = setUpDownVotes(request, puns)
        puns = orderQuerySetByPunScore(puns)
        context_dict['tag'] = tag
        context_dict['puns'] = puns

    except Tag.DoesNotExist:
        pass
    return render(request, 'punny/tag.html', context_dict)


def user_profile(request, username):
    if request.method == 'POST':
        form = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'new_pun_form': form, 'search_form': SearchForm()}
    try:
        u = User.objects.get(username=username)
        up = UserProfile.objects.filter(user__username__exact=username)
        title = Title.objects.filter(user__user=u)
        puns = Pun.objects.filter(Q(owner=u))
        totalScore = 0
        for pun in puns:
            pun.score = pun.rating.likes - pun.rating.dislikes
            totalScore += pun.score
        puns = setUpDownVotes(request, puns)
        puns = orderQuerySetByPunScore(puns)
        context_dict['user'] = u
        context_dict['userprofile'] = up
        context_dict['t'] = title
        context_dict['puns'] = puns
        context_dict['user_score'] = totalScore

    except UserProfile.DoesNotExist:
        pass
    return render(request, 'punny/profile.html', context_dict)


@login_required
def settings(request):
    if request.method == 'POST':
        form = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'new_pun_form': form, 'search_form': SearchForm()}
    return render(request, 'punny/user-settings.html', context_dict)

import slug as slug
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from punny.models import Pun, Tag, UserProfile, Badge, Title
import punny_search
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.models import User
from forms import PunForm
import re
import datetime


# Create your views here.

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
                  score=0,
                  NSFW=form.cleaned_data['NSFW'],
                  flagCount=0)
        pun.save()
        for tag in tagObjs:
            pun.tags.add(tag)
            # adding tag objects to the pun
    return form


def index(request):
    context = RequestContext(request)
    user = request.user
    if request.method == 'POST':
        form = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'form': form}
    context_dict['user'] = user
    return render(request, 'punny/index.html', context_dict)
    # return render(request, 'punny/index.html', {})


def search(request):
    if request.method == 'POST':
        form = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'form': form}
    query_string = ""
    puns = None
    if ('q' in request.POST) and request.POST['q'].strip():
        query_string = request.POST['q']

        # entry_query = punny_search.get_query(query_string, ['text', ])
        puns = Pun.objects.filter(Q(tags__text__icontains=query_string))

    context_dict['query_string'] = query_string
    context_dict['puns'] = puns

    return render_to_response('punny/search-results.html',
                              context_dict,
                              context_instance=RequestContext(request))

    # return render(request, 'punny/search-results.html', context_dict)


def tag_detail(request, tag_name_slug):
    context_dict = {}
    try:
        tag = Tag.objects.get(s=tag_name_slug)
        puns = Pun.objects.filter(Q(tags__text__exact=tag.text))
        context_dict['tag'] = tag
        context_dict['puns'] = puns

    except Tag.DoesNotExist:

        pass
    return render(request, 'punny/tag.html', context_dict)


def user_profile(request, username):
    context_dict = {}
    try:
        u = User.objects.get(username=username)
        up = UserProfile.objects.filter(user__username__exact=username)
        title = Title.objects.filter(user__user=u)
        puns = Pun.objects.filter(Q(owner=u))

        context_dict['user'] = u
        context_dict['userprofile'] = up
        context_dict['t'] = title
        context_dict['puns'] = puns

    except UserProfile.DoesNotExist:
        pass
    return render(request, 'punny/profile.html', context_dict)


@login_required
def settings(request):
    return render(request, 'punny/user-settings.html', {})

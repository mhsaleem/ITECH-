from django.template.defaultfilters import slugify
from watson import search as watson
from django.shortcuts import render, render_to_response
from models import Pun, Tag, UserProfile, Title
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from forms import PunForm, SearchForm, SettingsForm
from datetime import timedelta
from django.utils import timezone

import re
import datetime
import operator


def get_user_title_attributes(user):
    user_attr = {}
    puns = Pun.objects.filter(Q(owner=user))
    total_score = 0
    for pun in puns:
       pun.score = pun.rating.likes - pun.rating.dislikes
       total_score += pun.score
    user_attr['posts_num'] = puns.count()
    user_attr['score'] = total_score
    user_attr['time_in_days'] = timezone.now() - user.date_joined
    return user_attr

# Reusable function to process a pun submission
def process_pun_form(request):
    did_post = False
    form = PunForm(request.POST)
    if form.is_valid():
        # this is working, redirect needs fixed. But currently users do not have profiles automatically
        tags = re.split("; |, ", form.cleaned_data['tags'])
        # converting text to tag objects
        tag_objs = []
        for tag in tags:
            tag_objs.append(Tag.objects.get_or_create(text=tag)[0])

        pun = Pun(text=form.cleaned_data['puntext'],
                  owner=request.user,
                  NSFW=form.cleaned_data['NSFW'],
                  flagCount=0)
        with watson.update_index():
            pun.save()
        for tag in tag_objs:
            pun.tags.add(tag)
            # adding tag objects to the pun
        did_post = True
    return (form, did_post)


def get_all_tags_list():
    all_tags = Tag.objects.filter()
    texts = []
    for t in all_tags:
        texts.append(t.text)
    return texts


def set_up_down_votes(request, puns):
    if puns is not None:
        for pun in puns:
            pun.score = pun.rating.likes - pun.rating.dislikes
            x = pun.rating.get_rating_for_user(request.user)
            if x == 1:
                pun.upvoted = True
            elif x == -1:
                pun.downvoted = True
    return puns


def order_query_set_by_pun_score(puns):
    if puns is not None:
        for pun in puns:
            pun.score = pun.rating_likes - pun.rating_dislikes
        puns = sorted(puns, key=operator.attrgetter('score'), reverse=True)
        return puns


def get_top_puns_in_past_days(days=1):
    now = datetime.datetime.now()
    start_day = now - timedelta(days=days)
    puns = Pun.objects.filter(timeStamp__range=(start_day, now))
    if puns:
        puns = order_query_set_by_pun_score(puns)
        top_pun = puns[0]
        return top_pun
    else:
        return None

def get_trending_tags(days=1):
    now = datetime.datetime.now()
    start_day = now - timedelta(days=days)
    puns = Pun.objects.filter(timeStamp__range=(start_day, now))
    recent_tags = Tag.objects.filter(pun__tag=puns)
    return recent_tags


def index(request):
    did_post_pun = False
    user = request.user
    if request.method == 'POST':
        form, did_post_pun = process_pun_form(request)
    else:
        form = PunForm()

    context_dict = {'new_pun_form': form, 'user': user, 'search_form': SearchForm()}
    now = datetime.datetime.now()
    context_dict['tags'] = get_trending_tags(10)
    context_dict['today'] = get_top_puns_in_past_days(1)
    context_dict['week'] = get_top_puns_in_past_days(7)
    context_dict['month'] = get_top_puns_in_past_days(30)
    return render(request, 'punny/index.html', context_dict)


def search(request):
    did_post_pun = False
    if request.method == 'POST':
        form, did_post_pun = process_pun_form(request)
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
    if request.user.is_authenticated():
        puns = set_up_down_votes(request, puns)
    if puns is not None:
        puns = order_query_set_by_pun_score(puns)
        for pun in puns:
            pun.profile = UserProfile.objects.get(user=pun.owner)
    context_dict['tags_list'] = get_all_tags_list()
    context_dict['query_string'] = query_string
    context_dict['puns'] = puns
    response = render_to_response('punny/search-results.html',
                                  context_dict,
                                  context_instance=RequestContext(request))
    if did_post_pun:
        response.set_cookie('message', 'pun posted!', max_age=3)

    return response


def tag_detail(request, tag_name_slug):
    did_post_pun = False
    if request.method == 'POST':
        form, did_post_pun = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'new_pun_form': form, 'search_form': SearchForm()}
    try:
        tag_name_slug = slugify(tag_name_slug)
        tag = Tag.objects.get(s=tag_name_slug)
        puns = Pun.objects.filter(Q(tags__text__exact=tag.text))
        for pun in puns:
            pun.score = pun.rating_likes - pun.rating_dislikes
        if request.user.is_authenticated():
            puns = set_up_down_votes(request, puns)
        if puns.exists():
            #puns = order_query_set_by_pun_score(puns)
            for pun in puns:
                pun.profile = UserProfile.objects.get(user=pun.owner)
        context_dict['tag'] = tag
        context_dict['puns'] = puns

    except Tag.DoesNotExist:
        pass
    response = render(request, 'punny/tag.html', context_dict)
    if did_post_pun:
        response.set_cookie('message', 'pun posted!', max_age=3)

    return response


def user_profile(request, username):
    did_post_pun = False
    if request.method == 'POST':
        form, did_post_pun = process_pun_form(request)
    else:
        form = PunForm()
    context_dict = {'new_pun_form': form, 'search_form': SearchForm()}
    try:
        u = User.objects.get(username=username)
        up = UserProfile.objects.get(user__exact=u)
        x = up.picture
        puns = Pun.objects.filter(Q(owner=u))
        total_score = 0
        for pun in puns:
            pun.score = pun.rating.likes - pun.rating.dislikes
            total_score += pun.score
        if request.user.is_authenticated():
            puns = set_up_down_votes(request, puns)
        if puns.exists():
            puns = order_query_set_by_pun_score(puns)
            for pun in puns:
                pun.profile = UserProfile.objects.get(user=pun.owner)
        context_dict['page_user'] = u
        context_dict['userprofile'] = up
        context_dict['userprofile'] = up
        context_dict['puns'] = puns
        context_dict['user_score'] = total_score

    except UserProfile.DoesNotExist:
        pass
    response = render(request, 'punny/profile.html', context_dict)
    if did_post_pun:
        response.set_cookie('message', 'pun posted!', max_age=3)
    return response


@login_required
def settings(request):
    did_post_pun = False
    did_save_details = False
    user = request.user
    profile = UserProfile.objects.get(user=user)
    new_pun_form = PunForm()
    if request.method == 'POST':
        if request.POST.get("puntext"):  # if this a post with a new pun
            new_pun_form, did_post_pun = process_pun_form(request)
        else:
            form = SettingsForm(request.POST)
            tt = form['title']
            if form.is_valid():
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']  # check if the user actually uploaded a file
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.email = form.cleaned_data['email']
                profile.selected_title = Title.objects.get(title=form.cleaned_data['title'])
                profile.save()
                user.save()
                did_save_details = True
    context_dict = {'new_pun_form': new_pun_form, 'search_form': SearchForm()}
    settings_form = SettingsForm(initial={'username': user.username,
                                          'email': user.email,
                                          'firstname' : user.first_name,
                                          'lastname' : user.last_name,
                                          'title': profile.selected_title}, user=user)
    settings_form.fields['username'].widget.attrs[
        'readonly'] = True  # although an html/javascript wizard could override this, we're not atually storing any data anyhow
    user_attr = get_user_title_attributes(user)
    #checking what titles this user meets requirements for
    settings_form.fields['title'].choices = [(t.title, t.title) for t in Title.objects.filter(
                                                                                              min_number_days__lte=user_attr['time_in_days'].days,
                                                                                              min_score__lte=user_attr['score'],
                                                                                              min_number_posts__lte=user_attr['posts_num'])]
    context_dict['settings_form'] = settings_form
    context_dict['user'] = user
    context_dict['user_profile'] = profile

    response = render(request, 'punny/user-settings.html', context_dict)
    if did_post_pun:
        response.set_cookie('message', 'pun posted!', max_age=2)
    if did_save_details:
        response.set_cookie('saved', 'profile saved!', max_age=2)
    if (
        user.last_login - user.date_joined).seconds < 60:  # user registered less than sixty seconds ago. Display message for help
        response.set_cookie('virgin', 'this is a first time user', max_age=4)

    return response


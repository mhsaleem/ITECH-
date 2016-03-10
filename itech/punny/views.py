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

# Create your views here.

def index(request):
    return render(request, 'punny/index.html', {})
    # return render(request, 'punny/index.html', {})


def search(request):
    query_string = ""
    puns = None
    if ('q' in request.POST) and request.POST['q'].strip():
        query_string = request.POST['q']

        #entry_query = punny_search.get_query(query_string, ['text', ])
        puns = Pun.objects.filter(Q(tags__text__icontains=query_string))

        #puns = Pun.objects.filter(entry_query).order_by('-timeStamp')


    #puns = Pun.objects.order_by('-timeStamp')
    #context_dict = {'puns': puns}


    return render_to_response('punny/search-results.html',
                              {'query_string': query_string, 'puns': puns},
                              context_instance=RequestContext(request))

    #return render(request, 'punny/search-results.html', context_dict)


def tag_detail(request, tag_name_slug):
    context_dict={}
    try:
        tag = Tag.objects.get(s=tag_name_slug)
        puns = Pun.objects.filter(Q(tags__text__exact=tag.text))
        context_dict['tag'] = tag
        context_dict['puns'] = puns

    except Tag.DoesNotExist:

        pass
    return render(request, 'punny/tag.html', context_dict)


@login_required
def userProfile(request):
    return render(request, 'punny/user-profile.html', {})


@login_required
def settings(request):
    return render(request, 'punny/user-settings.html', {})

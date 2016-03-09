from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from punny.models import Pun, Tag, UserProfile, Badge, Title

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.

def index(request):
    return render(request, 'punny/index.html', {})
    # return render(request, 'punny/index.html', {})


def search(request):
    context_dict = {}
    puns = Pun.objects.order_by('-timeStamp')
    context_dict

    return render(request, 'punny/search-results.html', {})


@login_required
def userProfile(request):
    return render(request, 'punny/user-profile.html', {})

@login_required
def settings(request):
    return render(request, 'punny/user-settings.html', {})

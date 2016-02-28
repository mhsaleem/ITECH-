from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'punny/index.html', {})
    # return render(request, 'punny/index.html', {})

def search(request):
    return render(request, 'punny/searchResults.html', {})
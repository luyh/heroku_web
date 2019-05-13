from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from hpg.hpg3.hpg_request import HPG
import os,time

# Create your views here.
def index(request):

    # return HttpResponse('Hello from Python!')
    return render(request, "login.html")

def login(request):

    return HttpResponse('Hello from Python!')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

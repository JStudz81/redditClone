from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from . import  models
from django.core import validators
from django.core.exceptions import ValidationError
from . import forms
import logging
import urllib.parse
from django.contrib.auth.models import User

def index(request):
    loginForm = forms.LoginForm
    registerForm = forms.RegisterForm

    posts = models.Post.objects.all().order_by('-id')
    votes = models.Post

    context = {
        'loginForm': loginForm,
        'registerForm': registerForm,
        'user': request.user,
        'posts': posts
    }

    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/')
            else:
                # Return an 'invalid login' error message.
                return HttpResponseRedirect('/')

def createUser_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.create_user(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/')
            else:
                # Return an 'invalid login' error message.
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def create_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.PostForm(request.POST)
        url = validators.URLValidator()
        # check whether it's valid:
        try:
            url(urllib.parse.unquote(request.POST['link']))

            if form.is_valid():
                title = request.POST['title']
                text = request.POST['text']
                link = request.POST['link']
                post = models.Post(title=title, text=text, link=link)
                post.save()
            return HttpResponseRedirect('/')
        except ValidationError:
            return HttpResponseRedirect('/')
    elif request.method == 'GET':
        form = forms.PostForm
        return render(request, 'create.html', { 'form': form })

def vote_view(request, postId):
    post = models.Post.objects.get(id=postId)
    if not models.Vote.objects.filter(post=post, user=request.user):
        vote = models.Vote.objects.create(post=post, user=request.user)
        vote.save()

    return HttpResponseRedirect('/')

def test(request):
    return HttpResponse("wokring now")

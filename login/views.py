#coding:utf-8
from django.shortcuts import render
from django.contrib.auth import login as _login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as _logout
from django.http import HttpResponseRedirect, HttpResponse
from models import *
# Create your views here.

def login(request):
    hit = "None"
    if request.GET.get("next"):
        hit = "pleaseauth"
    return render(request, 'login.html', {'hit': hit })

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        _login(request, user)
        return HttpResponseRedirect("http://118.123.6.162:48000/info/")
    else:
        hit = "error"
        return render(request, 'login.html', {'hit': hit })

def logout(request):
    _logout(request)
    return HttpResponseRedirect("http://118.123.6.162:48000/")

def passport(request):
    return render(request, 'passport.html')

def registe(request):
    username = request.POST['username']
    password = request.POST['password']
    confirm = request.POST['confirm']
    code = request.POST['code']
    if code == "111111":
        if password == confirm:
            print password
        else:
            hit = "diff"
            return render(request, 'passport.html', {'hit': hit })
    else:
        hit = "nocode"
        return render(request, 'passport.html', {'hit': hit })
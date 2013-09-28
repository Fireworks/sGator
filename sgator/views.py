from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

def home(request):
    return render(request, "home.html")

def static_page(page, title):
    return lambda request: render(request, page, {"title": title})
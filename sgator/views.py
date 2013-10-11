from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from course.models import Course
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt   
from pyquery import PyQuery

import string

def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]

def home(request):
    return render(request, "home.html")

def static_page(page, title):
    return lambda request: render(request, page, {"title": title})

def search(request):
    query = request.GET.get('q')
    criteria = request.GET.get('DEPT')
    if criteria != " ":
        resultsF = Course.objects.filter(dept__exact = criteria)
    
    size = len(resultsF)      
    context = RequestContext(request)
    return render_to_response('courses.html', {"results": resultsF,"size": size}, context_instance=context)

@csrf_exempt 
def pasth(request):
    data = request.POST.get('test')
    context = RequestContext(request)
    results = list()
    pq = PyQuery(data)
    for c in pq('td'):
        results.append(pq(c).text())
        #to be parsed and added to Schedule Model when created

    return render_to_response('pasth.html', {"results": results,}, context_instance=context)
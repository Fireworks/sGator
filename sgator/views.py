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
import string

def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]

def home(request):
    return render(request, "home.html")

def static_page(page, title):
    return lambda request: render(request, page, {"title": title})

def search(request):
    query = request.GET.get('q')
    criteria = request.GET.get('c')
    if criteria == 'name':
         if not ' ' in query:
             tquery = insert_space(query, 3)
         else: tquery = query
             
         try:
            results = Course.objects.filter(name__iexact = tquery)
        
         except Course.DoesNotExist:
            results = Course.objects.all()

    if criteria == 'prefix':
        
         try:
            results = Course.objects.filter(name__icontains = query)
        
         except Course.DoesNotExist:
            results = Course.objects.all()
            
            
    if criteria == 'section':
         
         try:
            results = Course.objects.filter(section__icontains = query)
        
         except Course.DoesNotExist:
            results = Course.objects.all()

    if criteria == 'instr':
         if ' ' in query:
             tquery = query.rpartition(' ')[2]
         else: 
                tquery = query
         try:
            results = Course.objects.filter(cinst__icontains = tquery)
        
         except Course.DoesNotExist:
            results = Course.objects.all()



            
    context = RequestContext(request)
    size = len(results)
    return render_to_response('courses.html', {"results": results,"size": size}, context_instance=context)

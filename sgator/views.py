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

def home(request):
    return render(request, "home.html")

def static_page(page, title):
    return lambda request: render(request, page, {"title": title})

def search(request):
    query = request.GET.get('q')
    try:
        results = Course.objects.filter(name__contains = query)
        #results = Course.objects.all()
    except Course.DoesNotExist:
        results = Course.objects.all()  
    context = RequestContext(request)
    size = len(results)
    return render_to_response('courses.html', {"results": results,"size": size}, context_instance=context)

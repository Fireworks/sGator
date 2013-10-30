from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.http import HttpResponse
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
import json



def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]

def home(request):
    return render(request, "home.html")

 
def generateSchedule(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        if request.is_ajax():
            courses = request.raw_post_data
            request.user.get_profile().courses.append(courses)
            #todo: pass courses to algorithm
            return HttpResponse(courses)
        else:
            courses = request.user.get_profile().courses
            courseO = list() # list of courses based on given ID
            for i in courses:
                courseO.append(Course.objects.get(id__exact = i))
            return render_to_response('schedule.html', {"courses": courseO,}, context_instance=context)
        
    else:
        return render_to_response('nsi.html', context_instance=context)
    #ALGORITHM to be implemented or referenced here for this page
    
def profile(request):
    context = RequestContext(request)
    user_profile = request.user.get_profile()#profile object passed to template - can also be manipulated
    if request.user.is_authenticated():
        return render_to_response("profile.html",{"uprofile": user_profile,},context_instance=context)  # to be edited when more stuff is added to profile page
    else:
        return render_to_response('nsi.html', context_instance=context)

def static_page(page, title):
    return lambda request: render(request, page, {"title": title})  #Pages that don't need authentication

def search(request):
    context = RequestContext(request)
    iquery = request.GET.get('q')
    query = iquery.strip()
    criteria = request.GET.get('DEPT')
    #print query + str(len(query))
    if criteria != "":
        resultsF = Course.objects.filter(dept__exact = criteria)
        
    else:
        
        if len(query) == 3 or ((len(query) == 8 or len(query) == 9) and ' ' in query):
            resultsF = Course.objects.filter(name__icontains = query)
        elif (not query.isalpha()) and (len(query) == 7 or len(query) == 8):
            tquery = insert_space(query,3)
            resultsF = Course.objects.filter(name__icontains = tquery)
        elif len(query) == 4:
            resultsF = Course.objects.filter(section__icontains = iquery)
        elif len(query) == 2:
            return render_to_response('nrf.html', context_instance=context)  
        elif len(query) > 1:

            if ' ' in query:
                index = query.find(' ')
                tfname = query[index+1:]
                tlname = query[0:index]
                resultsF = Course.objects.filter(cinst__icontains = tlname).filter(cinst__icontains = tfname)
            else:
                resultsF = Course.objects.filter(cinst__icontains = query)
                
            
        else:
            return render_to_response('nrf.html', context_instance=context)  #temporary no results found page
                                          
    size = len(resultsF)    
    if size < 1:
        return render_to_response('nrf.html', context_instance=context)   
    return render_to_response('courses.html', {"results": resultsF,"size": size}, context_instance=context)




@csrf_exempt 
def pasth(request):
    context = RequestContext(request)
    if request.user.is_authenticated(): 
        data = request.POST.get('test')
        results = list()
        pq = PyQuery(data)
        for c in pq('td'):
            results.append(pq(c).text())
            #to be parsed and added to Schedule Model of User Profile Model when created
			
			 #"""
			 ## work in progress 
			 ##change above to get 'tr' 
			 #
			 ##begin by parsing variables from each course by each "td" 
			 #pastClass = Course(); 
			 #pastClass.name = c
			 #pastClass.section = c #0000 for transfer classes
			 #pastClass.cname = c
			 #pastClass.cedits = c
			
			 ##Put the course into a schedule object 
			 ## FOR NOW EVERY COURSE IS ITS OWN "SCHEDULE" ---> FIX LATER 
			 #tempSchedule = Schedule(); 
			 #tempSchedule.add(pastClass); 
			 #
			 ## create variable in userprofile to store these schedules
			 #courseHistory.append(tempSchedule); 
			"""
			
        return render_to_response('pasth.html', {"results": results,}, context_instance=context)

    else:
        return render_to_response('nsi.html', context_instance=context)

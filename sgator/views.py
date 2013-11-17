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
import algorithm


def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]

def home(request):
    return render(request, "home.html")

@csrf_exempt  
def generateSchedule(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        if request.is_ajax():  #Justin's Toast
            courses = request.raw_post_data
            request.user.get_profile().courses.append(courses)
            return HttpResponse(courses)
        else:
            tcourses = list()
            templist = list()
            if request.POST.get('clear'):
                del request.user.get_profile().cursc[0:len(request.user.get_profile().cursc)]  #CLEAR temporary list of schedules generated
            if request.POST.get('Generate'):
                #Make Call To algorithm here generate button was clicked
                tcourses = algorithm.get_results(request.user.get_profile().courses)   #temporary courses chosen added to queue per user not to be lost after refresh
                if len(tcourses) > 0:
                    results = algorithm.generate_schedules(tcourses)
                    #print results
                    request.user.get_profile().cursc.insert(0,results)  #place in current user schedule (temporary)
                    templist = list() #Translating Schedule Model back to Course model for template tag interpretation
                    for s in request.user.get_profile().cursc[0]: #Most recent generated schedule
                        templist2 = list()
                        for c in s.sections:
                            templist2.append(c)
                        templist.append(templist2)
                    del request.user.get_profile().courses[0:len(request.user.get_profile().courses)] #If generated, the temporary courses are removed from the table and the User object
            
                else:
                    templist = request.user.get_profile().cursc
                    templist2 = list()#Translating Schedule Model back to Course model for template tag interpretation
                    if len(templist) > 0:
                        for s in templist[0]:
                            templist3 = list()
                            for c in s.sections:
                                templist3.append(c)
                            templist2.append(templist3)
                    templist = templist2
                    
            else:
                templist = request.user.get_profile().cursc
                templist2 = list()#Translating Schedule Model back to Course model for template tag interpretation
                if len(templist) > 0:
                    
                    for s in templist[0]:
                        templist3 = list()
                        for c in s.sections:
                            templist3.append(c)
                        templist2.append(templist3)
                templist = templist2
                    
            courses = request.user.get_profile().courses
            courseO = list() # list of courses based on given ID for courses to be generated -> Cleared on generate!
            for i in courses:
                courseO.append(Course.objects.get(id__exact = i))
            return render_to_response('schedule.html', {"courses": courseO,"results": templist,}, context_instance=context)
        
    else:
        return render_to_response('nsi.html', context_instance=context)
  
    
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
        return render_to_response('pasth.html', {"results": results,}, context_instance=context)

    else:
        return render_to_response('nsi.html', context_instance=context)

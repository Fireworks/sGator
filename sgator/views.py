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
from sgator.models import Schedule
from sgator.algorithm import *
import string
import json
import algorithm
import models

def generateLinks(results):  #generate links for campus map view
    tempstrings = list()
    needed = ['name','lday','dday','ltime', 'dtime', 'lbuild', 'dbuild']
    tempstring = ''
    for course in results:
        for field, val in course:
            if field in needed:
                if (len(val) > 0) :
                    tempstring = tempstring + val +','
                    
        templist = tempstring.split(',')
        print templist
        x = len(templist) - 1
        y = 0
        while(x >=0):
            tempstrings.insert(x,templist[y])
            x = x-1
            y = y+1
            
        tempstring = tempstring + ';'
        
    print ''.join(tempstrings)
    
    return '0'

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
            generated = False
            clickSave = False
            saveIndex = 0
            action = None
            for key in request.POST.keys():
                if key.startswith('save:'):
                    action = key[5:]
                    #print 'SAVE' + str(action)
                    saveIndex = int(action)
                    clickSave = True
                    break
            if request.POST.get('clear'):
                del request.user.get_profile().cursc[0:len(request.user.get_profile().cursc)]  #CLEAR temporary list of schedules generated
                del request.user.get_profile().courses[0:len(request.user.get_profile().courses)] #If generated, the temporary courses are removed from the table and the User object
            courses = request.user.get_profile().courses
            courseO = list() # list of courses based on given ID for courses to be generated
            names = list()
            for i in courses:
                courseO.append(Course.objects.get(id__exact = i))
                if Course.objects.get(id__exact = i).name not in names:
                    names.append(Course.objects.get(id__exact = i).name) 
            namesF = list()
            for n in names:
                tlist = list()
                for c in courseO:
                    if c.name == n:
                        tlist.append(c)
                namesF.append(tlist)
            numFoundCourses = len(namesF) #automatically find number of wanted courses
            if request.POST.get('Generate'):
                if request.POST.get('numc'):
                    try:
                        numc = int(request.POST.get('numc'))
                    except:
                        numc = 20
                else: numc = 20
                generated = True
                tcourses = request.user.get_profile().courses   #temporary courses chosen added to queue per user not to be lost after refresh
                if len(tcourses) > 0:
                    if numc > len(namesF): # Where numc is number of courses put in by user
                        numc = len(namesF)
                    results = algorithm.generate_schedules(tcourses,numc)
                    for i in range(0,len(results)):
                        templist.insert(i,(results[i]))# for each schedule, get correct formatting for template tags, schedule1 ->templist(1) and so on....
                            #Need to insert formatdisplay() method for front end for posible new schedule list type
                    request.user.get_profile().cursc.insert(0,templist)  #place in current user schedule (temporary)

                else:
                    templist = request.user.get_profile().cursc      #hold value on refresh
            else:
                if generated:  
                    for s in request.user.get_profile().cursc:
                        for v in s:
                            templist.append(v)
                    generated = false
                else:
                    if len(request.user.get_profile().cursc) > 0:
                        templist = request.user.get_profile().cursc[0]  
                             
            actual = []
            if request.POST and not clickSave:
                print request.POST
                for result in templist:
                    good = True;
                    for cls in result:
                        print vars(cls)
                        if len(cls.lday.split()) > len([i for i in cls.lday.split() if i in dict(request.POST)['days']]):
                            good = False
                            break
                        if len(cls.dday.split()) > len([i for i in cls.dday.split() if i in dict(request.POST)['days']]):
                            good = False
                            break
                        for time in gettimes(cls.ltime):
                            print time
                            if time < int(request.POST['no_before']):
                                good = False
                            elif time > int(request.POST['no_after']):
                                good = False
                        for time in gettimes(cls.dtime):
                            print time
                            if time < int(request.POST['no_before']):
                                good = False
                            elif time > int(request.POST['no_after']):
                                good = False
                    if good:
                        actual.append(result)
                templist = actual
            if clickSave: 
                print actual
                request.user.get_profile().savedsch.append(templist[saveIndex - 1])
                print 'SAVED SCHEDULE NUMBER ' + str(saveIndex)
                print request.user.get_profile().savedsch

            return render_to_response('schedule.html', {"courses": courseO,"results": templist,"totalC":numFoundCourses,}, context_instance=context)
        
    else:
        return render_to_response('nsi.html', context_instance=context)
  
    
def profile(request):
    context = RequestContext(request)
    user_profile = request.user.get_profile()#profile object passed to template - can also be manipulated
    if request.user.is_authenticated():
        print request.user.get_profile().savedsch #saved schedules being passed
        return render_to_response("profile.html",{"uprofile": user_profile,"Schedule":request.user.get_profile().savedsch, },context_instance=context)  # to be edited when more stuff is added to profile page
    else:
        return render_to_response('nsi.html', context_instance=context)

def static_page(page, title):
    return lambda request: render(request, page, {"title": title})  #Pages that don't need authentication

def search(request):
    context = RequestContext(request)
    iquery = request.GET.get('q')
    query = iquery.strip()
    criteria = request.GET.get('DEPT')
    print query + str(len(query))
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
        coursesFound = 0;
        tempSchedule = Schedule()
        for c in pq('tr'):
            results.append(pq(c).text())
	
			#find out if this is class data
            query = "COURSE SECT GRADE CREDIT CREDIT EARNED CREDIT FOR GPA COURSE TITLE"
			
			
            if pq(c).text() == query: #go through the page to find when courses first appear 
				coursesFound = 1
				#print "found courses" #debug log
				
            else: #if it is not a header then do this
				if coursesFound == 1: #if it is not a header AND courses have already been found, parse them
					coursedata = pq(c)
					pastClass = Course() #temp class object 
					for d in coursedata('td'): # break the tr down into it's td values
						#print coursedata(d).text() #debugging logs 
						
						length = len(coursedata(d).text()) #get the length of the data so we know what field it is
						
						if length == 8:
							pastClass.name = coursedata(d).text()
						else: 
							if length == 4:
								 pastClass.section = coursedata(d).text() #0000 for transfer classes
							else:
								if length == 1 or length == 2:
									pastClass.finalgrade = coursedata(d).text() 
								else:
									if length == 3:
										pastClass.cedits = coursedata(d).text() #note: there can be multiple credit fields (credits earned, for gpa, credits), we are grabbing the very last one 
									else:
										pastClass.cname = coursedata(d).text()
					tempSchedule.add(pastClass)
						
        user_profile = request.user.get_profile()				
        user_profile.pastHistory = tempSchedule; #go to user profile and add tempschedule	
			
        return render_to_response('pasth.html', {"results": results,}, context_instance=context)

    else:
        return render_to_response('nsi.html', context_instance=context)

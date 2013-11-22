from django import template
from sgator.algorithm import *

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_display(results):
    cperiods = ([{} for i in range(14)], [])
    #pass through one schedule at a time from views
    
    for c in results:
        ltime = gettimes(c.ltime)
            #print ltime #get lecture times of each course
        dtime = gettimes(c.dtime)
            #print dtime #get discussion times of each course
        for t in ltime: #add to spot based on lecture time
            for day in c.lday.split():
                cperiods[0][t-1][day] = (c, False)
        for d in dtime: #add to spot based on discussion time
            for day in c.dday.split():
                cperiods[0][d-1][day] = (c, True) #true = is discussion
        if c.lday == 'TBA' or c.lroom == 'WEB':
        	cperiods[1].append(c)
    return cperiods
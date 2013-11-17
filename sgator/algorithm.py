from course.models import Course as DB_Course
from sgator.models import Schedule
import itertools

def get_results(Courses):
    # For the multi-dimension construction of Results to work, 
    # need to initialize a list of empty lists.
    Results = []
    for course in Courses:
        if course.isdigit(): # If a course entry has numbers, the user is requesting any section
            database_results = DB_Course.objects.filter(id = course)
        else: # If a course entry is just numbers, the user is requesting a specific section
            database_results = DB_Course.objects.filter(name__iexact = course)
        sections = []
        for result in database_results:
            lecture_days = lecture_times = discussion_days = discussion_times = []
            if result.lbuild == 'WEB': # Special handler for WEB lectures
                lecture_days = ['B']
                lecture_times = [0]
            elif not result.lday == ' ':
                lecture_days = [str(c) for c in result.lday if not c.isspace()]
                lecture_times = get_times(result.ltime)
            if result.dbuild == "WEB": # Special handler for WEB lectures
                discussion_days = ['B']
                discussion_times = [0]
            elif not result.dday == ' ':
                discussion_days = [str(c) for c in result.dday if not c.isspace()]
                discussion_times = get_times(result.dtime)
            times = list(itertools.product(lecture_days, lecture_times)) + list(itertools.product(discussion_days, discussion_times))
            sections.append((result, times))
        Results.append(sections)
    # At this point, Results contains all the sections of all the courses the user requested
    # With each course split into a dimension
    return Results

def get_times(ltime):
    if len(ltime)==4 and '-' not in ltime:
        ltime = ltime[0:2] + '-' + ltime[2:4]
    time_strings = [str(time) for time in ltime.split('-')]
    time_ints = []
    special_cases = {'E1':12, 'E2':13, 'E3':14, 'TBA':0}
    for element in time_strings:
        if element.isdigit():
            time_ints.append(int(element))
        if element in special_cases:
            time_ints.append(special_cases[element])
    if len(time_ints)==2:
        return range(time_ints[0], time_ints[1]+1)
    else:
        return time_ints
    
def formatDisplay(results):
    cperiods = [[] for i in range(14)]
    #pass through one schedule at a time from views
    
    for c in results.sections:
        ltime = get_times(c.ltime)
            #print ltime #get lecture times of each course
        dtime = get_times(c.dtime)
            #print dtime #get discussion times of each course
        for t in ltime: #add to spot based on lecture time
            try:
                cperiods[t-1].append(c) # for every period in that course, add it to that period list'
                    #print "ADDING L " + str(c) + " TO INDEX " + str(t)   
            except:
                cperiods[13].append(c) #edge cases excluded, added later in views
        for d in dtime: #add to spot based on discussion time
            try:
                cperiods[d-1].append(c) 
                    #print "ADDING D " + str(c) + " TO INDEX " + str(d)   
            except:
                cperiods[13].append(c)
    return cperiods

                
# example use: if( overlaps( Results[x][0], Results[x][1] ))
def overlaps(class1, class2):
    return any((t==t2 and not(t==('B', 0) or t2==('B', 0))) for t in class1[1] for t2 in class2[1])

def generate_schedules(Results):
    Possible_Schedules = []
    for possibility in itertools.product(*Results):
        if not all([overlaps(s1, s2) for s1, s2 in itertools.combinations(possibility, 2)]):
            schedule = Schedule()
            for course, times in possibility:
                schedule.add(course)
            Possible_Schedules.append(schedule)
    return Possible_Schedules

from course.models import Course as DB_Course
from sgator.models import Schedule

#Courses = [] # This is where we would get the list of Strings for the user's requested courses
#Results = [] # We will query the database to fill this list with each section for each course in Courses

def getResults(Courses):
    Results = []
    for course in Courses:
        course.replace(" ","") # Remove any spaces
        if course.isdigit(): # If a course entry has numbers, the user is requesting any section
            Results += list(DB_Course.objects.filter(id = course))
        else: # If a course entry is just numbers, the user is requesting a specific section
            Results += list(DB_Course.objects.filter(name__icontains = course)) # where section.name is the string name, ie "CEN3031"
    # At this point we should have a list of Courses in Jordan format
    for i in range(len(Results)):
        # split Results[i]/lday into list by ' 's, build list containing dictionary elements
        lecture_days = (c for c in Results[i].lday if c is not " ")
        lecture_time = Results[i].ltime
        discussion_days = (c for c in Results[i].dday if c is not " ")
        discussion_time = Results[i].dtime
        times = [{'day': day, 'time': time} for day, time in zip(lecture_days, lecture_time)] + [{'day': day, 'time': time} for day, time in zip(discussion_days, discussion_time)]
        Results[i] = (Results[i], times)
    return Results

# example use: if( overlaps( Results[0], Results[1] )
def overlaps(class1, class2):
    return any(t==t2 for t in class1[1] for t2 in class2[1])

# At this point, Results contains all the sections of all the courses the user requested
#Possible_Schedules = list(Schedule(x) for x in Results[i][0] if Results[i][0].
Possible_Schedules = []
# add all the partial schedules for the first course here...

#for i in range(1,len(Results)):
#    # add every section from Results that match Courses_[i], if they don't overlap
#    schedule = Schedule.__init__()
#    schedule.add(Results(i))
#    for j in range(1,len(Results)):
#        schedule.add(Results(j))
#        
#        
#    Possible_Schedules[i] = schedule

def generate_schedules(Results):
    schedule = Schedule.__init__()
    generate_schedules_helper(schedule,Results,1)

def generate_schedules_helper(schedule,Results,i):
    if i == len(Results): # base case
        Possible_Schedules[len(Possible_Schedules)] = schedule
    else:
        for j in range(1,len(Results)): # recursive case
            schedule2 = Schedule.__init__(schedule)
            if not overlaps(Results[i],Results[j]): # only make a new schedule if there is no conflict
                schedule2.add(Results[j])
                generate_schedules_helper(schedule2,j)

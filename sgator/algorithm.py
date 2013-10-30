from course.models import Course as DB_Course
from sgator.models import Schedule
import itertools

#Courses = [] # This is where we would get the list of Strings for the user's requested courses
#Results = [] # We will query the database to fill this list with each section for each course in Courses

def get_results(Courses):
    # For the multi-dimension construction of Results to work, 
    # need to initialize a list of empty lists.
    Results = []
    for course in Courses:
        course.replace(" ","") # Remove any spaces
        if course.isdigit(): # If a course entry has numbers, the user is requesting any section
            database_results = DB_Course.objects.filter(id = course)
        else: # If a course entry is just numbers, the user is requesting a specific section
            database_results = DB_Course.objects.filter(name__icontains = course)
        sections = []
        for result in database_results:
            lecture_days = (c for c in result.lday if c is not " ")
            lecture_time = result.ltime
            discussion_days = (c for c in result.dday if c is not " ")
            discussion_time = result.dtime
            times = [{'day': day, 'time': time} for day, time in zip(lecture_days, lecture_time)] + [{'day': day, 'time': time} for day, time in zip(discussion_days, discussion_time)]
            sections.append((result, times))
        Results.append(sections)
    # At this point, Results contains all the sections of all the courses the user requested
    # With each course split into a dimension
    return Results

# example use: if( overlaps( Results[x][0], Results[x][1] )
def overlaps(class1, class2):
    return any(t==t2 for t in class1[1] for t2 in class2[1])

#for i in range(1,len(Results)):
#    # add every section from Results that match Courses_[i], if they don't overlap
#    schedule = Schedule.__init__()
#    schedule.add(Results(i))
#    for j in range(1,len(Results)):
#        schedule.add(Results(j))
#    Possible_Schedules[i] = schedule

def generate_schedules(Results):
    Possible_Schedules = []
    schedule = Schedule.__init__()
    Possible_Schedules.extend(generate_schedules_helper(Results,0))
    return Possible_Schedules

def generate_schedules_helper(Results,i):
    possibles = []
    if i == len(Results): # base case
        return possibles
    for j in range(len(Results[i])):
         
        possibles.append(schedule)
    else:
        # If element i+1 !overlap and is not same course, add it to schedule
        # If element i+1 !overlap and is same course, but is different dl, add to sched
        # If element i+1 !overlap and is same course, but is same dl, make new schedule

        if (not overlaps(Results[i],Results[i+1])):
           if ( 
                possibles.extend( generate_schedules_helper(
    return possibles

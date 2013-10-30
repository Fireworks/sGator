from course.models import Course as DB_Course
from sgator.models import Schedule
import itertools

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

def generate_schedules(Results):
    Possible_Schedules = []
    schedule = Schedule()
    for possibility in itertools.product(*Results):
        if all(not overlaps(s1, s2) for s1, s2 in itertools.combinations(possibility, 2)):
            Possible_Schedules.append(possibility)
    return Possible_Schedules

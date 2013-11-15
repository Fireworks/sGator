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
        print database_results
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
    r = [str(time) for time in ltime.split('-')]
    s = []
    for element in r:
        if element.isdigit():
            s.append(int(element))
        elif element == "E1":
            s.append(12)
        elif element == "E2":
            s.append(13)
        elif element == "E3":
            s.append(14)
    times = []
    for i in range(s[len(s)-1] - s[0] + 1): 
        times.append(int(str(s[0])) + i)
    return times

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

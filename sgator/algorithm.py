from course.models import Course as DB_Course
from sgator.models import Schedule

Courses = [] # This is where we would get the list of Strings for the user's requested courses
Results = [] # We will query the database to fill this list with each section for each course in Courses
# If a course entry has numbers, the user is requesting any section of that class
# If a course entry is just numbers, the user is requesting a specific section of a class
for course in Courses:
    Results += list(DB_Course.objects.filter(name__icontains = course)) # where section.name is the string name, ie "CEN 3031"
# At this point we should have a list of Courses in Jordan format
for i in range(len(Results)):
    # split Results[i]/lday into list by ' 's
    # build list containing dictionary elements
    lecture_days = (c for c in Results[i].lday if c is not " ")
    lecture_time = Results[i].ltime
    discussion_days = (c for c in Results[i].dday if c is not " ")
    discussion_time = Results[i].dtime
    times = [{'day': day, 'time': time} for day, time in zip(lecture_days, lectures_time)] +
            [{'day': day, 'time': time} for day, time in zip(discussion_days, discussion_time)]
    Results[i] = (Results[i], times)

# At this point, Results contains all the sections of all the courses the user requested
Possible_Schedules = []
# add all the partial schedules for the first course here...

for i in range(1,len(Courses)):
    # add every section from Results that match Courses_[i], if they don't overlap

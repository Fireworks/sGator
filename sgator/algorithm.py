from course.models import Course

# This part gets the list of sections we need
Results = []
# Sections is the list of courses requested by the user
for section in Sections:
    Results += list(Course.objects.filter(name__icontains = section.name)) # where section.name is the string name, ie "CEN 3031"
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


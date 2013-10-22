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
    times = [{'day': x, 'time': y} for x, y in zip((c for c in Results[i].lday if c is not " "), Results[i].ltime)]
    times.update(dict(zip((c for c in Results[i].dday if c is not " "), Results[i].dtime)))
    Results[i] = (Results[i], times)


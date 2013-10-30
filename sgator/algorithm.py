from course.models import Course as DB_Course
from sgator.models import Schedule

#Courses = [] # This is where we would get the list of Strings for the user's requested courses
#Results = [] # We will query the database to fill this list with each section for each course in Courses

def get_results(Courses):
    # For the multi-dimension construction of Results to work, 
    # need to initialize a list of empty lists.
    Results = []
    for x in range(len(Courses)):
        res.append([]) 
    num_courses = 0
    for course in Courses:
        course.replace(" ","") # Remove any spaces
        if course.isdigit(): # If a course entry has numbers, the user is requesting any section
            piece = list(DB_Course.objects.filter(id = course))
        else: # If a course entry is just numbers, the user is requesting a specific section
            piece = list(DB_Course.objects.filter(name__icontains = course))
        for i in range(len(piece)):
            lecture_days = (c for c in piece[i].lday if c is not " ")
            lecture_time = piece[i].ltime
            discussion_days = (c for c in piece[i].dday if c is not " ")
            discussion_time = piece[i].dtime
            times = [{'day': day, 'time': time} for day, time in zip(lecture_days, lecture_time)] + [{'day': day, 'time': time} for day, time in zip(discussion_days, discussion_time)]
            discussion_flag = 0 # Set a flag equal to 1 if the section is a discussion
            if (piece[i].lday = '') 
                discussion_flag = 1
            piece[i] = (Results[i], times, discussion_flag)
            Results[num_courses].extend(piece[i])
            num_courses += 1
    # At this point, Results contains all the sections of all the courses the user requested
    return Results

# example use: if( overlaps( Results[x][0], Results[x][1] )
def overlaps(class1, class2):
    return any(t==t2 for t in class1[1] for t2 in class2[1])

# example use: if( samecourse( Results[y][0], Results[y][1] )
# Returns True if both classes are the same course by name
def samecourse(class1, class2):
    return class1[0].name == class2[0].name

# example use: if( both_dl( Results[z][0], Results[z][1] )
# Returns True if both classes are discussions or both are lectures
def both_dl(class1, class2):
    return class1[2] == class2[2]

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

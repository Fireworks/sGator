from course.models import Course as DB_Course
from sgator.models import Schedule
from course.models import Course
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
                lecture_times = gettimes(result.ltime)
            if result.dbuild == "WEB": # Special handler for WEB lectures
                discussion_days = ['B']
                discussion_times = [0]
            elif not result.dday == ' ':
                discussion_days = [str(c) for c in result.dday if not c.isspace()]
                discussion_times = gettimes(result.dtime)
            times = list(itertools.product(lecture_days, lecture_times)) + list(itertools.product(discussion_days, discussion_times))
            sections.append((result, times))
        Results.append(sections)
    # At this point, Results contains all the sections of all the courses the user requested
    # With each course split into a dimension
    return Results

def gettimes(ltime):
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
        ltime = gettimes(c.ltime)
            #print ltime #get lecture times of each course
        dtime = gettimes(c.dtime)
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

def generate_schedules(Results,numc):
    #NOW passing through only ONE list of combinations, a 1D list of course IDs
    blank = list()
    list3 = list()
    '''
    IDcombo = itertools.combinations(Results,numc) # number of combinations will depend on how many courses people want //OLD DONT TOUCH
    
    finalL = list()
    for i in IDcombo:
            finalL.append(i)
    '''
    for v in Results:
        list2.append(findID(v))  #findID will be changed to return values from database based on ID of course, 

        if  not checkDup(list2): #remove duplicate names from iterations passed ->not possible to have more than one of same class
            list3.append(list2)
    if len(list3) > 0:
        return checkConflict(list3) #contains combination passed from Jonathan's input_subset IF there are no duplicates
    else: return blank
    #IF there are duplicates in the combinations results will return a blank list length 0 
    
def findID(i): #will query database to find and return given courses, in this case source is just a list passed from the beginning
    return Course.objects.get(id__iexact = i)



def checkConflict(list1):
    count = 0
    btemp = list()
    temp = list()
    btemp = checkLect(list1)
    btemp = checkDisc(btemp)
    #print "CONSOLIDATED LIST " + str(btemp)
   #CHECK SEPARATELY FIRST  for Lecture and DIscussion conflicts -> Now we have all possible combinations based on ONLY Lecture vs Lecture and Disc vs Disc conflicts
    
    
    for i,lst in enumerate(btemp):
        size = len(lst) - 1
        x = size
        conflict = False
        while(size >=0):
            tempObject = lst[x] # index of comparator object
            for index,v in enumerate(lst):
                if index != x :
                    #print "CHECKING " + str(tempObject) + " and " + str(v)
                    (c1Lc2DT, c1Dc2LT) =  checkTime(tempObject,v,'B')    #Making sure only necessary conflicts are matched and not allowed
                    (c1Lc2DD, c1Dc2LD) = checkDay(tempObject,v,'B') 
                    if (c1Lc2DT and c1Lc2DD) or (c1Dc2LT and c1Dc2LD):
                            conflict = True
                            #print "Conflict with Course " + str(tempObject) + str(tempObject.id) +" AND " + str(v) + str(v.id)
                    else: count = count + 1
                #print conflict
            size = size - 1
            x = size -1
            #if count == 15:  #Here is where we set max number of schedules to display/give to the user
                #return temp
        #print "CONFLICT BEFORE APPEND" + str(conflict)
        #print str(len(temp))
        if not conflict:
            temp.append(lst)
            
   #THEN KNOW WHEN CHECKING DISCUSSION/LECTURE AND VICE VERSA
        
    return temp
        
    
def checkLect(list1):#Generic method to check only for lecture conflicts and elminate based on that
    temp = list()
    conflict = False
    x = len(list1) - 1
    while(x >= 0):
        templist = list1[x]
        #print "templist = " + str(templist)
        conflict = False
        y = len(templist) - 1
        while(y >= 0):
            tempc = templist[y]
            for c in templist:
                if tempc.name != c.name:
                    if checkTime(tempc,c,'L') and checkDay(tempc,c,'L'):
                        #print "Conflict with Course " + str(tempc) + str(tempc.id) +" AND " + str(c) + str(c.id)
                        conflict = True
                   

            y = y-1
        if not conflict:
            temp.append(templist)
        x = x-1
        
    return temp
        
def getdays(d):
    temp = list(d)
    temp2 = list()
    for c in temp:
        if c is not " ":
            temp2.append(c)
 
    return temp2



def checkDisc(list1): #Generic method to check only for discussion conflicts and elminate based on that
    temp = list()
    conflict = False
    x = len(list1) - 1
    while(x >= 0):
        templist = list1[x]
        conflict = False
        #print "templist = " + str(templist)
        y = len(templist) - 1
        while(y >= 0):
            tempc = templist[y]
            for c in templist:
                if tempc.name != c.name:
                    if checkTime(tempc,c,'D') and checkDay(tempc,c,'D'):
                        #print "Conflict with Course " + str(tempc) + str(tempc.id) +" AND " + str(c) + str(c.id)
                        conflict = True
                    

            y = y-1
        if not conflict:
            temp.append(templist)
        x = x-1
        
    return temp



def checkTime(c1,c2,t):# Check for Lecture/Discussion TIME conflicts
    if t == 'L': #check LECTURE vs LECTURE Conflicts ONLY
        c1time = gettimes(c1.ltime)
        c2time = gettimes(c2.ltime)
        for c in c1time:
            for t in c2time:
                if c == t:
                    return True
        
        
    elif t == 'D': #check DISCUSSION vs DISCUSSION Conflicts ONLY
        c1time = gettimes(c1.dtime)
        c2time = gettimes(c2.dtime)
        for c in c1time:
            for t in c2time:
                #print "Course 1 Time" + c + "Course 2 Time" + t+ "  "
                if c == t:
                    #print "CONFLICT"
                    return True

    elif t == 'B':#Check for BOTH LECTURE AND DISCUSSION MIXED CONFLICTS
        c1ltime = gettimes(c1.ltime)
        c2dtime = gettimes(c2.dtime)
        c1dtime = gettimes(c1.dtime)
        c2ltime = gettimes(c2.ltime)
        c1Lc2DT = False
        c1Dc2LT = False
        
        for c in c1ltime:   #C1 LECTURES VS C2 DISCUSSIONS TIMES
            for t in c2dtime:
                #print "Course 1 Time" + c + "Course 2 Time" + t+ "  "
                if c == t:
                    #print "CONFLICT "+ str(c1)+" LECTURES VS "+str(c2)+" DISCUSSIONS TIMES"
                    c1Lc2DT = True
                    

        for c in c2ltime:   #C2 LECTURES VS C1 DISCUSSIONS TIMES
            for t in c1dtime:
                #print "Course 1 Time" + c + "Course 2 Time" + t+ "  "
                if c == t:
                    #print "CONFLICT "+ str(c2)+" LECTURES VS "+str(c1)+" DISCUSSIONS TIMES"
                    c1Dc2LT = True
                    
        return (c1Lc2DT, c1Dc2LT)
    
    return False

def checkDay(c1,c2,t):# Check for Lecture/Discussion DAY conflicts
    if t == 'L':            #check LECTURE vs LECTURE Conflicts ONLY
        c1day = getdays(c1.lday)
        c2day = getdays(c2.lday)
        for c in c1day:
            for t in c2day:
                if c == t:
                    return True
        
        
    elif t == 'D':               #check DISCUSSION vs DISCUSSION Conflicts ONLY
        c1day = getdays(c1.dday)
        c2day = getdays(c2.dday)
        for c in c1day:
            for t in c2day:
                #print "Course 1 Day" + c + "Course 2 Day" + t+ "  "
                if c == t:
                    #print "CONFLICT"
                    return True


    elif t == 'B': #Check for BOTH LECTURE AND DISCUSSION MIXED CONFLICTS
        c1lday = gettimes(c1.lday)
        c2dday  = getdays(c2.dday)
        c1dday  = getdays(c1.dday)
        c2lday  = getdays(c2.lday)
        c1Lc2DD = False
        c1Dc2LD = False
        
        for c in c1lday :   #C1 LECTURES VS C2 DISCUSSIONS DAYS
            for t in c2dday :
                #print "Course 1 Time" + c + "Course 2 Time" + t+ "  "
                if c == t:
                    #print "CONFLICT "+ str(c1)+" LECTURES VS "+str(c2)+" DISCUSSIONS DAYS"
                    c1Lc2DD = True
                    

        for c in c2lday :   #C2 LECTURES VS C1 DISCUSSIONS DAYS
            for t in c1dday :
                #print "Course 1 Time" + c + "Course 2 Time" + t+ "  "
                if c == t:
                    #print "CONFLICT "+ str(c2)+" LECTURES VS "+str(c1)+" DISCUSSIONS DAYS"
                    c1Dc2LD = True
                    
                

        

        return (c1Lc2DD, c1Dc2LD)
    
    return False

def checkDup(listt):
    conflict = False
    x = len(listt) - 1
    while(x >= 0):
        tempc = listt[x]
        count = 0
        for v in listt:
            if tempc.name == v.name:
                count = count+1
                if count > 1:
                    return True
        x = x-1
        
    return conflict



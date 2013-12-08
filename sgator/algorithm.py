from course.models import Course as DB_Course
from sgator.models import Schedule
from course.models import Course
import itertools

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

def generate_schedules(Results,numc):
    finalL = list()
    list3 = list()
    IDcombo = itertools.combinations(Results,numc) # number of combinations will depend on how many courses people want
    for i in IDcombo:
            finalL.append(i)
    for l in finalL:
        list2 = list()
        for v in l:
            list2.append(findID(v))  
        if  not checkDup(list2): #remove duplicate names from iterations generated-> not possible to have more than one of same class
            list3.append(list2)
    return checkConflict(list3) #contains list of all combinations (lists) of courses without duplicate names
    
def findID(i): #will query database to find and return given courses, in this case source is just a list passed from the beginning
    return Course.objects.get(id__iexact = i)

def checkConflict(list1):
    btemp = list()
    temp = list()
    btemp = checkLectDisc(list1)
    print "CONSOLIDATED LIST " + str(btemp)
   #CHECK SEPARATELY FIRST  for Lecture and DIscussion conflicts -> Now we have all possible combinations based on ONLY Lecture vs Lecture and Disc vs Disc conflicts    
    for i,lst in enumerate(btemp):
        size = len(lst) - 1
        x = size
        conflict = False
        while(size >=0):
            tempObject = lst[x] # index of comparator object
            for index,v in enumerate(lst):
                if index != x :
                    (c1Lc2DT, c1Dc2LT) =  checkTime(tempObject,v,'B')    #Making sure only necessary conflicts are matched and not allowed
                    (c1Lc2DD, c1Dc2LD) = checkDay(tempObject,v,'B') 
                    if (c1Lc2DT and c1Lc2DD) or (c1Dc2LT and c1Dc2LD):
                            conflict = True
            size = size - 1
            x = size -1 
        if not conflict:
            temp.append(lst)   
   #THEN KNOW WHEN CHECKING DISCUSSION/LECTURE AND VICE VERSA        
    return temp   

def checkLectDisc(list1):#Generic method to check only for lecture conflicts and elminate based on that
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
                        conflict = True
                    if checkTime(tempc,c,'D') and checkDay(tempc,c,'D'):
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

def checkTime(c1,c2,t):# Check for Lecture/Discussion TIME conflicts
    c1Lc2DT = False
    c1Dc2LT = False
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
                if c == t:
                    return True

    elif t == 'B':#Check for BOTH LECTURE AND DISCUSSION MIXED CONFLICTS
        c1ltime = gettimes(c1.ltime)
        c2dtime = gettimes(c2.dtime)
        c1dtime = gettimes(c1.dtime)
        c2ltime = gettimes(c2.ltime)
        c1dtime2 = gettimes(c1.d2time)
        c2dtime2 = gettimes(c2.d2time)
        
        for c in c1ltime:   #C1 LECTURES VS C2 DISCUSSIONS TIMES
            for t in c2dtime:
                if c == t:
                    c1Lc2DT = True
                                
            for t in c2dtime2:
                if c == t:
                    c1Lc2DT = True
                    
        for c in c2ltime:   #C2 LECTURES VS C1 DISCUSSIONS TIMES
            for t in c1dtime:
                if c == t:
                    c1Dc2LT = True

            for t in c1dtime2:
                if c == t:
                    c1Dc2LT = True
                    
        return (c1Lc2DT, c1Dc2LT)
    
    return False

def checkDay(c1,c2,t):# Check for Lecture/Discussion DAY conflicts
    c1Lc2DD = False
    c1Dc2LD = False
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
                if c == t:
                    return True
                
    elif t == 'B': #Check for BOTH LECTURE AND DISCUSSION MIXED CONFLICTS
        c1lday = gettimes(c1.lday)
        c2dday  = getdays(c2.dday)
        c1dday  = getdays(c1.dday)
        c2dday2  = getdays(c2.d2day)
        c1dday2  = getdays(c1.d2day)
        c2lday  = getdays(c2.lday)

        for c in c1lday :   #C1 LECTURES VS C2 DISCUSSIONS DAYS
            for t in c2dday :
                if c == t:
                    c1Lc2DD = True
                    
            for t in c2dday2 :
                if c == t:
                    c1Lc2DD = True
                    
        for c in c2lday :   #C2 LECTURES VS C1 DISCUSSIONS DAYS
            for t in c1dday :
                if c == t:
                    c1Dc2LD = True

            for t in c1dday2 :
                if c == t:
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



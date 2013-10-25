from django.db import models
#from algorithm import overlaps

class Schedule(models.Model):
    def __init__(self):
        self.sections = []
        self.credits = models.CharField(max_length=200, default='0')
        # total credits in schedule

    def add(self,course):
#        for x in range(len(self.sections)):
#            if overlaps(course,self.sections(x)):
#                return False
        self.sections[course.section] = course
        self.credits = self.credits + course.credits
#        return True

    def remove(self,course):
        del self.sections[course.section]
        self.credits = self.credits - course.credits
        # subtract out credits of course

    def returnSchedule(self):
        return self.sections.values()

    def returnCredits(self):
        return self.credits

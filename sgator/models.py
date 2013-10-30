from django.db import models

class Schedule(models.Model):
    def __init__(self):
        self.sections = []
        self.credits = models.CharField(max_length=200, default='0')
        # total credits in schedule

    def add(self,course):
        self.sections.append(course)
        #self.credits += course.cedits

    def remove(self,course):
        del self.sections[course.section]
        self.credits = self.credits - course.credits
        # subtract out credits of course

    def returnSchedule(self):
        return self.sections.values()

    def returnCredits(self):
        return self.credits

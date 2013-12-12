from django.db import models

class Schedule(models.Model):
    def __init__(self):
        self.sections = []
        self.credits = models.CharField(max_length=200, default='0')
        # total credits in schedule
        self.averageRMP = models.CharField(max_length=200, default='0')
        # average rate my prof. score

    def add(self,course):
        self.sections.append(course)
        self.averageRMP = (self.averageRMP * self.credits + course.rmpr) / (self.credits + course.cedits)
        self.credits += course.cedits

    def remove(self,course):
        del self.sections[course.section]
        self.credits = self.credits - course.cedits
        # subtract out credits of course

    def __unicode__(self):
        return str(self.sections)

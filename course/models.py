from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    section = models.CharField(max_length=200)
    cname = models.CharField(max_length=200)
    lday = models.CharField(max_length=200)
    ltime = models.CharField(max_length=200)
    dday = models.CharField(max_length=200)
    dtime = models.CharField(max_length=200)
    dbuild = models.CharField(max_length=200)
    droom = models.CharField(max_length=200)
    lroom = models.CharField(max_length=200)
    cedits = models.CharField(max_length=200)
    lbuild = models.CharField(max_length=200)
    cinst = models.CharField(max_length=200)
    
    
    def __unicode__(self):  
        return self.name

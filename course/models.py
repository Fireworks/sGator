from django.db.models.signals import post_save
from django.contrib.auth.models import User
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
    dept = models.CharField(max_length=200)
   
    def __unicode__(self):  
        times = ""
        if not lday == "":
            times += "{} {}".format(lday, ltime)
        if not dday == "":
            times += ", {} {}".format(dday, dtime)
        return "{} section {}, {}".format(name, section, times)

class UserProfile(models.Model):
    pastsc = models.CharField(max_length=200 ) #Schedule Model to replace Charfield
	#courseHistory=models.Schedule()[]  make an array of past schedules?
    cursc = models.CharField(max_length=200 )
    user = models.ForeignKey(User, unique=True)
    facebook_id = models.CharField(max_length=200 )
    facebook_email = models.CharField(max_length=200 )
#tentative userprofile fields to be changed
    
    def __unicode__(self):
        return self.user.username + "'s User Profile"
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

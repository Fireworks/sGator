from django.db.models.signals import post_save
from django.db.models.signals import class_prepared
from django.contrib.auth.models import User
from django.db import models
from django_facebook.models import FacebookModel
from sgator.models import Schedule

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
    cedits = models.CharField(max_length=200) #  this is credits? not changing name to not mess others parts of site up
    lbuild = models.CharField(max_length=200)
    cinst = models.CharField(max_length=200)
    dept = models.CharField(max_length=200)
    rmpr = models.CharField(max_length=200)
    d2day = models.CharField(max_length=200)
    d2time = models.CharField(max_length=200)
    d2build = models.CharField(max_length=200)
    d2room = models.CharField(max_length=200)
    finalgrade = models.CharField(max_length=200) 
    
    def __unicode__(self):
        times = ""
        if not self.lday == "":
            times += "{} {}".format(self.lday, self.ltime)
        if not self.dday == "":
            times += ", {} {}".format(self.dday, self.dtime)
        if not self.d2day == "":
            times += ", {} {}".format(self.d2day, self.d2time)
        return "{} section {}, {}".format(self.name, self.section, times)
    
    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))
         


class UserProfile(FacebookModel):
    pastHistory = Schedule()#Schedule Model 
    cursc = list()
    courses = list()
    user = models.ForeignKey(User, unique=True)
   

    def __unicode__(self):
        return self.user.username + "'s User Profile"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



post_save.connect(create_user_profile, sender=User)


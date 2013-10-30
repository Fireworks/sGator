from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django_facebook.models import FacebookModel

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
    rmpr = models.CharField(max_length=200)
    
    def __unicode__(self):
        time = ""
        if not self.lday == "":
            times += "{} {}".format(self.lday, self.ltime)
        if not self.dday == "":
            times += ", {} {}".format(self.dday, self.dtime)
        return "{} section {}, {}".format(self.name, self.section, times)

class UserProfile(FacebookModel):
    pastsc = models.CharField(max_length=200 ) #Schedule Model to replace Charfield
    cursc = models.CharField(max_length=200 )
    courses = list()
    user = models.ForeignKey(User, unique=True)
    #facebook_id = models.BigIntegerField(blank=True, unique=True, null=True)
    #facebook_email = models.CharField(max_length=200 )
    #tentative userprofile fields to be changed

    def __unicode__(self):
        return self.user.username + "'s User Profile"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

from django.db import models

class Section(models.Model):
    # Necessary for building schedules
    name = models.CharField(max_length=200)
    section = models.CharField(max_length=200)
    DAYS_OF_WEEK = ('M', 'T', 'W', 'R', 'F')
    PERIODS = map(str, range(1,12)) + ['E1', 'E2', 'E3']
    times = models.CharField(max_length=2, choices=DAYS_OF_WEEK, PERIODS)
    # Example of times:
    # time = [{'day':'M', 'time':5}, {'day':'W', 'time':5}, {'day':'F', 'time':5}]

    # Extra fields for display
    lecture_or_discussion = models.CharField(max_length=200) # To clarify for display purposes
    course_full_name = models.CharField(max_length=200)
    building = models.CharField(max_length=200)
    room = models.CharField(max_length=200)
    credits = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def is_overlapping(self, other):
        for t in self.times:
            for t2 in other.times:
                if t['day'] == t2['day'] && t['time'] == t2['time']:
                    return True
        return False

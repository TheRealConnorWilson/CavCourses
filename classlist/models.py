from email.policy import default
from unittest.util import _MAX_LENGTH
from xmlrpc.client import DateTime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
# Create your models here.

""" 
Whenever making a new model, make sure to run:
python manage.py makemigrations
python manage.py migrate
"""

"""
Citations:
Title: DateTimeField - Django Models
URL: https://www.geeksforgeeks.org/datetimefield-django-models/

Title: Step by Step guide to add friends with Django
Sections: Friend Request Model
URL: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d

"""

class Account(models.Model): 
    """
    Represents each user's account in the database
    Reference for models.User: https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#user-model
    """
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    USERNAME_FIELD = models.CharField(max_length=150, default="User") # something was demanding this be USERNAME_FIELD instead of username
    first_name = models.CharField(max_length=150, blank=True, default="User") # blank=True means that it is optional
    last_name = models.CharField(max_length=150, blank=True, default="Name")
    email = models.EmailField(max_length=150, default="none@gmail.com")
    # password = models.CharField(max_length=150) # not sure if we need to store this?
    last_login = models.DateTimeField('last date logged in', default=timezone.now)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_authenticated = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)
    
    avatar = models.URLField(default='/static/classlist/default_account_image.png')
    account_created = models.BooleanField(default=False) # currently not used
    
    # friends fields
    friends = models.ManyToManyField("Account", related_name='my_friends', blank=True)
    # sent_friend_requests = models.ManyToManyField("Account", related_name = 'from_user', blank=True)
    # received_friend_requests = models.ManyToManyField("Account", related_name = 'to_user', blank=True)
    
    # account info
    #schedule = models.ManyToManyField("Section", blank=True)
    major = models.CharField(max_length=100, default=True)
    
    FIRST_YEAR = 1
    SECOND_YEAR = 2
    THIRD_YEAR = 3
    FOURTH_YEAR = 4
    OTHER = 5
    
    YEAR_IN_SCHOOL_CHOICES = [
        (FIRST_YEAR, 'First year'),
        (SECOND_YEAR, 'Second year'),
        (THIRD_YEAR, 'Third year'),
        (FOURTH_YEAR, 'Fourth year'),
        (OTHER, 'Other')
    ]
    
    year = models.IntegerField(choices=YEAR_IN_SCHOOL_CHOICES,default=OTHER)

    def get_username(self):
        return self.username
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    def get_short_name(self):
        return self.first_name
    def get_authenticated(self):
        return self.is_authenticated
    
    def __str__(self):
        return self.email
class Friend_Request(models.Model):
    # call two user models
    from_user = models.ForeignKey(Account, related_name = 'from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Account, related_name = 'to_user', on_delete=models.CASCADE)
    
    # from_user = models.IntegerField(default=0)
    # to_user = models.IntegerField(default=0)
    
    def __str__(self):
        return str("Request from " + str(self.from_user) + " to " + str(self.to_user)) 

class Instructor(models.Model):
    name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=100, blank=True)

    @classmethod
    def get_default_instructor(self):
        default_instructor = Instructor.objects.get_or_create(name="No Instuctor Specified", email = "N/A")[0]
        return default_instructor.pk

    def __str__(self):
        return self.name
class Department(models.Model):
    """
    Represents a department at UVA
    """
    dept_abbr = models.CharField(max_length=100)
    last_updated = models.DateTimeField("last updated", default=timezone.now)

    @classmethod
    def get_default_dept(self):
        default_dept =  Department.objects.get_or_create(dept_abbr="NULL")[0] # dept_abbr CANNOT be longer than 4 characters -- will break database!
        return default_dept.pk

    def __str__(self):
        return self.dept_abbr
class Course(models.Model):
    # refernce for how to add classes to sqlite with shell: https://docs.djangoproject.com/en/4.1/intro/tutorial02/
    last_updated = models.DateTimeField('date updated', default=timezone.now)
    catalog_number = models.CharField(max_length=100)
    semester_code = models.IntegerField(default=0) # ex. 1228
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True) # Introduction to Information Technology,
    units = models.CharField(max_length=100, blank=True) # 3, number of credits
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=Department.get_default_dept)
    subject = models.CharField(max_length = 100, blank=True)
    # sections = []

    # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.ordering
    # allows ListView to know how to order instances?
    ordering = ['department', 'catalog_number'] 
    
    @classmethod
    def get_default_course(self):
        default_course = Course.objects.get_or_create(
            last_updated = timezone.now,
            catalog_number = 0,
            semester_code = 0, # ex. 1228
            title = "N/A", # CS 1110
            description = "N/A", # Introduction to Information Technology,
            units = "", # 3, number of credits
            department = Department.get_default_dept(),
            subject = "",
            # sections = []
            )[0]
        return default_course.pk

    def __str__(self):
        return self.title # + str(self.catalog_number)
class Section(models.Model):
    # additional model fields so that a section knows what course it belongs to
    course_dept = models.CharField(max_length = 100, blank=True)
    course_num = models.CharField(max_length = 100, blank=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)

    section_id = models.IntegerField(default=0, primary_key=True) # ex. 16351
    section_number = models.CharField(max_length = 100, blank=True) # 001
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=Instructor.get_default_instructor)
    component = models.CharField(max_length=100, blank=True) # LEC,
    capacity = models.IntegerField(default=0) # 75,
    wait_list = models.IntegerField(default=0) # 0
    wait_cap = models.IntegerField(default=0) # 199,
    enrollment_total = models.IntegerField(default=0) # 72,
    enrollment_available = models.IntegerField(default=0) # 3
    topic = models.CharField(max_length=200, blank=True)
    # meetings = []

    def __str__(self):
        return str(self.section_id) + ": " + str(self.section_number) + " - " + self.component
        
class Meetings(models.Model):
    days = models.CharField(max_length=100, blank=True) # MoWeFr, -
    start_time = models.CharField(max_length=100, blank=False, default="00.00.00.000000-05:00") # 17.00.00.000000-05:00
    end_time = models.CharField(max_length=100, blank=False, default="00.00.00.000000-05:00") # 18.15.00.000000-05:00
    facility_description = models.CharField(max_length=200, blank=True) # Olsson Hall 009
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True)
    
    # fields for storing which days the class meets on -- assuming no classes meet on sat/sun?
    # use days field to fill them out in view
    monday = models.BooleanField(blank=True, default=False)
    tuesday = models.BooleanField(blank=True, default=False)
    wednesday = models.BooleanField(blank=True, default=False)
    thursday = models.BooleanField(blank=True, default=False)
    friday = models.BooleanField(blank=True, default=False)
    saturday = models.BooleanField(blank=True, default=False)
    sunday = models.BooleanField(blank=True, default=False)

    def days_of_the_week(self):
        days = [(2, self.monday), 
                (3, self.tuesday), 
                (4, self.wednesday), 
                (5, self.thursday), 
                (6, self.friday), 
                (7, self.saturday), 
                (8, self.sunday)]
        return days
    

    # @classmethod
    # def get_default_meeting():
    #     return Meetings.objects.get_or_create(days="N/A", start_time="N/A", end_time="N/A", facility_description="N/A")[0]

    def start_time_as_date_time(self):
        if self.start_time != "":
            start_time_split = self.start_time.split('.')
            return start_time_split[0] + ":" + start_time_split[1]
        return "00:00"

    def end_time_as_date_time(self):
        if self.end_time != "":
            end_time_split = self.end_time.split('.')
            return end_time_split[0] + ":" + end_time_split[1]
        return "00:00"

    # for calculating positioning of classes in schedule
    # def x_position(self):

    HEADER_HEIGHT = 2

    def y_position(self):
        start_time = self.start_time_as_date_time().split(":")
        hour = int(start_time[0]) * 60
        minutes = int(start_time[1])

        print(start_time, hour, minutes)

        return hour + minutes + self.HEADER_HEIGHT
    
    def length(self):
        start = self.y_position()
        end_time = self.end_time_as_date_time().split(":")
        hour = int(end_time[0]) * 60
        minutes = int(end_time[1])
        end = hour + minutes + self.HEADER_HEIGHT

        # print(end, hour, minutes)

        return end - start

    def __str__(self):
        return self.days + ": " + self.start_time + "-" + self.end_time + " @ " + self.facility_description

    ordering = ['start_time',]
    
# class Friend_Request(models.Model):
#     # call two user models
#     # from_user = models.ForeignKey(User, related_name = 'from_user', on_delete=models.CASCADE)
#     # to_user = models.ForeignKey(User, related_name = 'to_user', on_delete=models.CASCADE)
    
#     from_user = models.IntegerField(default=0)
#     to_user = models.IntegerField(default=0)
    
#     def __str__(self):
#         return str("Request from " + str(self.from_user) + " to " + str(self.to_user))

class Schedule(models.Model):

    # who owns the schedule?
    #scheduleUser = models.ForeignKey(Account, related_name = 'user_schedule', on_delete=models.CASCADE)
    scheduleUser = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True, default=None)

    # many-to-many field relating to a specific section of a course - allows for multiple classes
    classRoster = models.ManyToManyField("Section", related_name='user_course', blank=True, default=None)

    def __str__(self):
        return str(self.scheduleUser)

    def __unicode__(self):
        return str(self.scheduleUser)


class Comment(models.Model):
    from_user = models.ForeignKey(Account, related_name="my_comments", on_delete=models.CASCADE, blank=True)
    to_user = models.ForeignKey(Account, related_name="schedule_comments", on_delete=models.CASCADE, blank=True)
    # schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True)
    text = models.CharField(max_length=250)
    
    def __str__(self) -> str:
        return self.text

from email.policy import default
from unittest.util import _MAX_LENGTH
from xmlrpc.client import DateTime
from django.db import models

from django.utils import timezone
from django.contrib import admin
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
"""

class User(models.Model): 
    """
    Represents each user in the database
    Reference for models.User: https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#user-model
    """
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, blank=True) # blank=True means that it is optional
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150)
    # password = models.CharField(max_length=150) # not sure if we need to store this?
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    is_authenticated = True
    is_anonymous = False

    # schedule = []

    def get_username(self):
        return self.username
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    def get_short_name(self):
        return self.first_name
    def get_authenticated(self):
        return self.is_authenticated

    # class_list = []

class Instructor(models.Model):
    name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=25, blank=True)

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
    dept_abbr = models.CharField(max_length=4)

    @classmethod
    def get_default_dept(self):
        default_dept =  Department.objects.get_or_create(dept_abbr="No Department Specified")[0]
        return default_dept.pk

    def __str__(self):
        return self.dept_abbr

class Course(models.Model):
    # refernce for how to add classes to sqlite with shell: https://docs.djangoproject.com/en/4.1/intro/tutorial02/
    last_updated = models.DateTimeField('date updated', default=timezone.now)
    catalog_number = models.CharField(max_length=4)
    semester_code = models.IntegerField(default=0) # ex. 1228
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True) # Introduction to Information Technology,
    units = models.CharField(max_length=20, blank=True) # 3, number of credits
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=Department.get_default_dept)
    subject = models.CharField(max_length = 4, blank=True)
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
    course_dept = models.CharField(max_length = 4, blank=True)
    course_num = models.IntegerField(default=0)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)

    section_id = models.IntegerField(default=0) # ex. 16351
    section_number = models.CharField(max_length = 4, blank=True) # 001
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=Instructor.get_default_instructor)
    component = models.CharField(max_length=20, blank=True) # LEC,
    capacity = models.IntegerField(default=0) # 75,
    wait_list = models.IntegerField(default=0) # 0
    wait_cap = models.IntegerField(default=0) # 199,
    enrollment_total = models.IntegerField(default=0) # 72,
    enrollment_available = models.IntegerField(default=0) # 3
    topic = models.CharField(max_length=200, blank=True) # optional description | This may belong in course
    # meetings = []

    def __str__(self):
        return str(self.section_id) + ": " + str(self.section_number) + " - " + self.component


class Meetings(models.Model):
    days = models.CharField(max_length=10, blank=True) # MoWeFr
    start_time = models.CharField(max_length=100, blank=True) # 17.00.00.000000-05:00
    end_time = models.CharField(max_length=100, blank=True) # 18.15.00.000000-05:00
    facility_description = models.CharField(max_length=200, blank=True) # Olsson Hall 009
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True)

    # @classmethod
    # def get_default_meeting():
    #     return Meetings.objects.get_or_create(days="N/A", start_time="N/A", end_time="N/A", facility_description="N/A")[0]

    def start_time_as_date_time(self):
        if self.start_time != "":
            start_time_split = self.start_time.split('.')
            return start_time_split[0] + ":" + start_time_split[1]
        return self.start_time

    def end_time_as_date_time(self):
        if self.end_time != "":
            end_time_split = self.end_time.split('.')
            return end_time_split[0] + ":" + end_time_split[1]
        return self.end_time

    def __str__(self):
        return self.days + ": " + self.start_time + "-" + self.end_time + " @ " + self.facility_description
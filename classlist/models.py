from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
import datetime

from django.utils import timezone
from django.contrib import admin
# from django.contrib.auth.models import User
# Create your models here.

""" 
Whenever making a new model, make sure to run:
python manage.py makemigrations
python manage.py migrate
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

    def get_username(self):
        return self.username
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    def get_short_name(self):
        return self.first_name
    def get_authenticated(self):
        return self.is_authenticated

    class_list = []


class Class(models.Model):
    # refernce for how to add classes to sqlite with shell: https://docs.djangoproject.com/en/4.1/intro/tutorial02/
    

    instructor = {
            "name": models.CharField(max_length=200, blank=True),
            "email": models.CharField(max_length=200, blank=True)
        }
    
    course_number = models.IntegerField(default=0) # ex. 16351
    semester_code = models.IntegerField(default=0) # ex. 1228
    course_section = models.IntegerField(default=0) # 001
    subject = models.CharField(max_length=20, blank=True) # CS
    catalog_number = models.IntegerField(blank=True, default=0) # 1010
    description = models.CharField(max_length=200, blank=True) # Introduction to Information Technology,
    units = models.IntegerField(default=0) # 3, number of credits
    component = models.CharField(max_length=20, blank=True) # LEC,
    class_capacity = models.IntegerField(default=0) # 75,
    wait_list = models.IntegerField(default=0) # 0
    wait_cap = models.IntegerField(default=0) # 199,
    enrollment_total = models.IntegerField(default=0) # 72,
    enrollment_available = models.IntegerField(default=0) # 3
    topic = models.CharField(max_length=200, blank=True) # optional description
    meetings = [
        {
            "days": models.CharField(blank=True), # MoWe,
            "start_time": models.CharField(blank=True), # 17.00.00.000000-05:00,
            "end_time": models.CharField(blank=True), # 18.15.00.000000-05:00,
            "facility_description": models.CharField(blank=True), #Olsson Hall 009
        }
    ]

    # class_title = subject + " " + catalog_number + ": " + description
    
    # description = models.CharField(max_length=200)
    # Credits = models.IntegerField()
    def __str__(self):
        return self.subject + " " + str(self.catalog_number) + ": " + self.description

    
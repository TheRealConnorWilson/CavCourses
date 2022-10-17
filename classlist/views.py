from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView
from datetime import datetime
from .models import User, Course, Department

import requests


"""
Citations:
Title: Python + Django page redirect
URL: https://stackoverflow.com/questions/523356/python-django-page-redirect

Title: How to get logged in username in views.py in django
URL: https://stackoverflow.com/questions/39785934/how-to-get-logged-in-username-in-views-py-in-django
"""

def index(request):
    return HttpResponseRedirect("/home")

def view_name(request):
    # ex. http://127.0.0.1:8000/accounts/google/login/
    template_name = "classlist/google_login.html"
    # return HttpResponseRedirect("/accounts/google/login")
    # model = User # need to make a user model
    # print(User.get_full_name(User))
    user = request.user 
    
    # options for login page
    # return HttpResponse("This is the login page!")

    context = {
        'user' : user,
    }
    
    return render(request, template_name, context)

def view_home(request):
    template_name = "classlist/home.html"
    return render(request, template_name)

def get_courses_by_dept(dept_abbr):
    # get all courses in a department
    template_name = "classlist/classes_by_dept.html"
    context_object_name = "courses_by_dept"

    #Access API
    api_url = "http://luthers-list.herokuapp.com/api/dept/" + dept_abbr + "/?format=json"
    dept_json = requests.get(api_url)
    dept_courses = dept_json.json()
    
    if(Department.objects.filter(dept_abbr=dept_abbr).exists()):
        dept = Department.objects.get(dept_abbr=dept_abbr)
    else:
        dept = Department(dept_abbr=dept_abbr)
        dept.save()

    #Assign all fields
    for course in dept_courses:
        course = Course(
            last_updated = datetime.now(),
            instructor = course["instructor"],
            course_number = course["course_number"],
            semester_code = course["semester_code"],
            course_section = course["course_section"],
            subject = course["subject"],
            catalog_number = course["catalog_number"],
            description = course["description"],
            units = course["units"],
            component = course["component"],
            class_capacity = course["class_capacity"],
            wait_list = course["wait_list"],
            wait_cap = course["wait_cap"],
            enrollment_total = course["enrollment_total"],
            enrollment_available = course["enrollment_available"],
            topic = course["topic"],
            meetings = course["meetings"],
        )
        dept.dept_classes.add(course)

    return dept.dept_classes # return all courses in a department

# first very basic view
class CourseView(generic.ListView):
    template_name = 'classlist/class.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all()

class DepartmentView(generic.ListView):
    template_name = 'classlist/classes_by_dept.html'
    context_object_name = 'department'

    def get_courses_by_dept(self):
        return get_courses_by_dept(self.dept_abbr)

    def get_queryset(self):
        return Department.objects.all()
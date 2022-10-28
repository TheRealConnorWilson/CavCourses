from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView
from .models import Meetings, Instructor, User, Course, Department, Section

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

###########
def get_depts(request):
    template_name = "classlist/class.html"

    #Access API
    api_url = "http://luthers-list.herokuapp.com/api/deptlist?format=json"
    depts_json = requests.get(api_url)
    all_depts = depts_json.json()
    
    return render(request, template_name, {"all_depts":all_depts})
###########


def get_courses_by_dept(request, dept_abbr):
    template_name = "classlist/classes_by_dept.html"
    
    #Access API
    api_url = "http://luthers-list.herokuapp.com/api/dept/" + dept_abbr + "/?format=json"
    dept_json = requests.get(api_url)
    all_dept_classes = dept_json.json()
    
    if(Department.objects.filter(dept_abbr=dept_abbr).exists()):
        dept = Department.objects.get(dept_abbr=dept_abbr)
    else:
        dept = Department(dept_abbr=dept_abbr)
        dept.save()

    # return render(request, template_name, {"all_dept_classes":all_dept_classes})


    #Assign all fields
    # if len(Course.objects.filter(subject = dept_abbr).order_by('department', 'catalog_number')) == 0:
    for course in all_dept_classes:
        
        instructor_name = course["instructor"]["name"]
        instructor_email = course["instructor"]["email"]
        
        if(Instructor.objects.filter(name=instructor_name, email=instructor_email).exists()):
            instructor_obj = Instructor.objects.get(name=instructor_name, email=instructor_email)
        else:
            instructor_obj = Instructor(name=instructor_name, email=instructor_email)
            instructor_obj.save()

        update_timestamp = timezone.now()
        sem_code = course["semester_code"]
        course_title = course["subject"] + " " + course["catalog_number"]
        course_description = course["description"]
        num_units = course["units"]
        catalog_num = course['catalog_number']

        if(Course.objects.filter(title=course_title).exists()):
            course_obj = Course.objects.get(title=course_title)
            course_obj.catalog_number = catalog_num
            # course_obj.sections = []
        else:
            course_obj = Course(title=course_title,
                                description=course_description,
                                units=num_units,
                                semester_code = sem_code,
                                last_updated = update_timestamp,
                                department = dept,
                                subject = course["subject"],
                                # sections = [],
                                catalog_number = catalog_num
                                )
            course_obj.save()


        section_id = course["course_number"]
        section_num = course["course_section"]
        course_component = course["component"]
        section_capacity = course["class_capacity"]
        section_wait_list = course["wait_list"]
        section_wait_cap = course["wait_cap"]
        section_enrollment = course["enrollment_total"]
        section_available_enrollment = course["enrollment_available"]
        section_topic = course["topic"]

        section_dept = course["subject"]
        section_course_num = course["catalog_number"]

        if(Section.objects.filter(section_id=section_id).exists()):
            section = Section.objects.get(section_id=section_id)
        else:
            section = Section(
                course_dept = section_dept,
                course_num = section_course_num,
                section_id = section_id,
                section_number = section_num,
                instructor = instructor_obj,
                component = course_component,
                capacity = section_capacity,
                wait_list = section_wait_list,
                wait_cap = section_wait_cap,
                enrollment_total = section_enrollment,
                enrollment_available = section_available_enrollment,
                topic = section_topic, #This may belong in course
                course = course_obj
                )
            section.save()

        meetings = course["meetings"]

        for meeting in meetings:
            meeting_days = meeting["days"]
            meeting_start_time = meeting["start_time"]
            meeting_end_time = meeting["end_time"]
            meeting_location = meeting["facility_description"]
        
            if(Meetings.objects.filter(days=meeting_days, start_time=meeting_start_time, end_time=meeting_end_time, facility_description=meeting_location).exists()):
                meetings_obj = Meetings.objects.get(days=meeting_days, start_time=meeting_start_time, end_time=meeting_end_time, facility_description=meeting_location)
            else:
                meetings_obj = Meetings(days=meeting_days,
                                        start_time=meeting_start_time,  
                                        end_time=meeting_end_time,
                                        facility_description=meeting_location,
                                        section = section
                                        )
                meetings_obj.save()
        
        
        course_obj.save()

    all_courses = Course.objects.filter(subject = dept_abbr).order_by('department', 'catalog_number')
    
    dept_context = {"dept" : dept,
                    "dept_abbr" : dept.dept_abbr,
                    "dept_courses" : all_courses,
                    }

    return render(request, template_name, context=dept_context)


# first very basic view
class CourseView(generic.ListView):
    template_name = 'classlist/class.html'
    context_object_name = 'departments'

    def get_queryset(self):
        # return Course.objects.all().order_by('department', 'catalog_number')
        return Department.objects.all().order_by('dept_abbr')

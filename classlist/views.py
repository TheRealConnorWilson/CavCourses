import re
from xml.dom import UserDataHandler
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView
from urllib3 import HTTPResponse
from .models import Meetings, Instructor, Account, Course, Department, Section
from django.contrib.auth import get_user_model
from .forms import UserAccountForm
from .forms import SearchForm

import requests


"""
Citations:
Title: Python + Django page redirect
URL: https://stackoverflow.com/questions/523356/python-django-page-redirect

Title: How to get logged in username in views.py in django
URL: https://stackoverflow.com/questions/39785934/how-to-get-logged-in-username-in-views-py-in-django

Title: Step by Step guide to add friends with Django
URL: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d

Title: How to Pass Additional Context into a Class Based View (Django)?
URL: https://www.geeksforgeeks.org/how-to-pass-additional-context-into-a-class-based-view-django/
"""

class AuthenticatedListView(generic.ListView):
    """
    Extend this version of ListView so that the header/page will be able to access the user's account information for the header and such!
    """
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context.update(get_user_info(self.request))
        return context
    


def index(request):
    return HttpResponseRedirect("/home")

def get_user_info(request):
    """
    This function generates a context that includes the user's matching account information for rendering the templates in other views
    """
    if request.user.is_authenticated:
        account = Account.objects.get(email=request.user.email)
        # print(account)
        context = {
            'user' : account,
        }
        return context
    else:
        return {}

def view_name(request):
    # ex. http://127.0.0.1:8000/accounts/google/login/
    template_name = "classlist/google_login.html"
    # return HttpResponseRedirect("/accounts/google/login")
    # model = User # need to make a user model
    # print(User.get_full_name(User))
    user = request.user 
    
    # options for login page
    # return HttpResponse("This is the login page!")
    if request.user.is_authenticated:
        if not Account.objects.filter(email=request.user.email).exists():
            return HttpResponseRedirect("/home")

    context = get_user_info(request)
    
    return render(request, template_name, context)
    # return HttpResponseRedirect("/accounts/google/login")

def view_home(request):
    """
    Allows the user to view the home page, takes into account the login status of the user
    - if the user is not logged in: directs them to view the departments page (they can still browse)
    - if the user is logged in but hasn't created an account yet: directs them to account creation page
    - if the user has an account: loads the home page and welcomes them
    """
    template_name = "classlist/home.html"
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/list")
    
    elif not Account.objects.filter(email=request.user.email).exists():
        return HttpResponseRedirect("/create_account")
    
    else: 
        account = Account.objects.get(email=request.user.email)
        # print(account)
        context = context = get_user_info(request)
        return render(request, template_name, context)

###########
def get_depts(request):
    template_name = "classlist/class.html"

    #Access API
    api_url = "http://luthers-list.herokuapp.com/api/deptlist?format=json"
    depts_json = requests.get(api_url)
    all_depts = depts_json.json()
    

    if request.method == 'POST':
        form = SearchForm(request.POST)
    else:
        form = SearchForm()

    if form.is_valid():
        for d in all_depts:
            if d['subject'] == form.cleaned_data.get('searched_dept'):
                dept_dict = {}
                dept_dict['subject'] = d['subject']
                all_depts = []
                all_depts.append(dept_dict)
                break

    return render(request, 'classlist/class.html', {'form':form, "all_depts":all_depts})
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

        # this was causing an issue with KINE 2000, where both meetings wouldn't show
        # trying live loading for section as well 
        
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
            meeting_section = section
            if meeting_location == "-":
                meeting_location = "TBA"
            
            # this was causing an issue with KINE 2000, where both meetings wouldn't show, made it so each meeting would pair with an individual section
            if(Meetings.objects.filter(days=meeting_days, start_time=meeting_start_time, end_time=meeting_end_time, facility_description=meeting_location, section=section).exists()):
                meetings_obj = Meetings.objects.get(days=meeting_days, start_time=meeting_start_time, end_time=meeting_end_time, facility_description=meeting_location, section=section)
            else:
                meetings_obj = Meetings(days=meeting_days,
                                        start_time=meeting_start_time,  
                                        end_time=meeting_end_time,
                                        facility_description=meeting_location,
                                        section = meeting_section
                                        )
            meetings_obj.save()
            
        
        course_obj.save()

    all_courses = Course.objects.filter(subject = dept_abbr).order_by('department', 'catalog_number')
    
    if request.user.is_authenticated:
        dept_context = {"dept" : dept,
                    "dept_abbr" : dept.dept_abbr,
                    "dept_courses" : all_courses,
                    'user' : Account.objects.get(email=request.user.email),
                    }
    else:
        dept_context = {"dept" : dept,
                        "dept_abbr" : dept.dept_abbr,
                        "dept_courses" : all_courses,
                        }

    return render(request, template_name, context=dept_context)


class CourseView(AuthenticatedListView):
    template_name = 'classlist/class.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.all().order_by('dept_abbr')
    
    
class ViewAccount(AuthenticatedListView):
    model = Account
    template_name = 'classlist/view_account.html'

class ViewUsers(AuthenticatedListView):
    """
    Allows users to view the other users on the site and potentially friend them
    TODO improve HTML layout
    
    """
    model = Account
    template_name = 'classlist/view_users.html'
    context_object_name = 'all_accounts'
    
    def get_queryset(self):
        return Account.objects.all()
    
def create_account(request):
    """
    Asks the user to input a username, major, and year
    Once submitted, it creates an account for them on the site
    
    TODO check for invalid submissions
    TODO add warning messages/error messages
    TODO add drop downs for HTML
    """
    # print(request.user.username, request.user.email)
    if request.method == 'POST':
        new_account = Account(USERNAME_FIELD=request.POST['username'], 
                            email=request.user.email, 
                            first_name=request.user.first_name,
                            last_name=request.user.last_name,
                            date_joined=timezone.now(),
                            is_authenticated=True,
                            major=request.POST['major'],
                            year=request.POST['year']
                            )
        new_account.save()
        return HttpResponseRedirect('/home')
        
    else:     
        # If this is a GET (or any other method) create the default form.
        form = UserAccountForm(initial={'USERNAME_FIELD': request.user.username, 'year': "Unknown", 'major': "Unknown", 'last_login' : timezone.now, 'date_joined' : timezone.now})
        
    return render(request, 'classlist/create_account.html', {'form': form})
    

def send_friend_request(request, userID): # ,userID
    """
    Creates a relation/model for a friend request between two users
    
    TODO 
    
    """
        
    created = False
    my_account = Account.objects.filter(email=request.user.email)
    their_account = Account.objects.filter(pk=userID)
    
    # if(my_account.friends):
    #     print("exists")
    #     course_obj = Course.objects.get(title=course_title)
    #     course_obj.catalog_number = catalog_num
    #     course_obj.sections = []
    # else:
    #     friend_request = Friend_Request(from_user=from_user_id, to_user=userID)
    #     friend_request.save()
    #     created = True
    #     print("yay")
    # if created:
    #     return HttpResponse('friend request sent')
    # else:
    #     return HttpResponse('friend request was already sent')
    
    
    

def accept_friend_request(request, requestID):
    """
    TODO 
    """
    print("hi")
    # friend_request = Friend_Request.objects.get(id=request)
    # if friend_request.to_user == request.user:
    #     friend_request.to_user.friends.add(friend_request.from_user)
    #     friend_request.from_user.friends.add(friend_request.to_user)
    #     friend_request.delete()
    #     return HTTPResponse('friend request accepted')
    # else:
    #     return HTTPResponse('friend request not accepted')
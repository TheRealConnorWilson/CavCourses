from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView
from urllib3 import HTTPResponse
from .models import Meetings, Instructor, Account, Course, Department, Section, Schedule, Friend_Request
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import UserAccountForm
from .forms import SearchForm, AdvancedSearchForm

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

Title: django: Purpose of django.utils.functional.SimpleLazyObject?
URL: https://stackoverflow.com/questions/10506766/django-purpose-of-django-utils-functional-simplelazyobject/10507200#10507200
"""

def get_user(request):
        """
        Title: django: Purpose of django.utils.functional.SimpleLazyObject?
        URL: https://stackoverflow.com/questions/10506766/django-purpose-of-django-utils-functional-simplelazyobject/10507200#10507200

        Use this in place of request.user, as that returns a lazy unactivated object
        """
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

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
    all_depts_search = []

    a_depts = []
    for d in all_depts:
        if d['subject'][0] == 'A':
            a_depts.append(d['subject'])
    b_depts = []
    for d in all_depts:
        if d['subject'][0] == 'B':
            b_depts.append(d['subject'])
    c_depts = []
    for d in all_depts:
        if d['subject'][0] == 'C':
            c_depts.append(d['subject'])
    d_depts = []
    for d in all_depts:
        if d['subject'][0] == 'D':
            d_depts.append(d['subject'])
    e_depts = []
    for d in all_depts:
        if d['subject'][0] == 'E':
            e_depts.append(d['subject'])
    f_depts = []
    for d in all_depts:
        if d['subject'][0] == 'F':
            f_depts.append(d['subject'])
    g_depts = []
    for d in all_depts:
        if d['subject'][0] == 'G':
            g_depts.append(d['subject'])
    h_depts = []
    for d in all_depts:
        if d['subject'][0] == 'H':
            h_depts.append(d['subject'])
    i_depts = []
    for d in all_depts:
        if d['subject'][0] == 'I':
            i_depts.append(d['subject'])
    j_depts = []
    for d in all_depts:
        if d['subject'][0] == 'J':
            j_depts.append(d['subject'])
    k_depts = []
    for d in all_depts:
        if d['subject'][0] == 'K':
            k_depts.append(d['subject'])
    l_depts = []
    for d in all_depts:
        if d['subject'][0] == 'L':
            l_depts.append(d['subject'])
    m_depts = []
    for d in all_depts:
        if d['subject'][0] == 'M':
            m_depts.append(d['subject'])
    n_depts = []
    for d in all_depts:
        if d['subject'][0] == 'N':
            n_depts.append(d['subject'])
    o_depts = []
    for d in all_depts:
        if d['subject'][0] == 'O':
            o_depts.append(d['subject'])
    p_depts = []
    for d in all_depts:
        if d['subject'][0] == 'P':
            p_depts.append(d['subject'])
    q_depts = []
    for d in all_depts:
        if d['subject'][0] == 'Q':
            q_depts.append(d['subject'])
    r_depts = []
    for d in all_depts:
        if d['subject'][0] == 'R':
            r_depts.append(d['subject'])
    s_depts = []
    for d in all_depts:
        if d['subject'][0] == 'S':
            s_depts.append(d['subject'])
    t_depts = []
    for d in all_depts:
        if d['subject'][0] == 'T':
            t_depts.append(d['subject'])
    u_depts = []
    for d in all_depts:
        if d['subject'][0] == 'U':
            u_depts.append(d['subject'])
    v_depts = []
    for d in all_depts:
        if d['subject'][0] == 'V':
            v_depts.append(d['subject'])
    w_depts = []
    for d in all_depts:
        if d['subject'][0] == 'W':
            w_depts.append(d['subject'])
    x_depts = []
    for d in all_depts:
        if d['subject'][0] == 'X':
            x_depts.append(d['subject'])
    y_depts = []
    for d in all_depts:
        if d['subject'][0] == 'Y':
            y_depts.append(d['subject'])
    z_depts = []
    for d in all_depts:
        if d['subject'][0] == 'Z':
            z_depts.append(d['subject'])
            


    if request.method == 'POST':
        form = SearchForm(request.POST)
    else:
        form = SearchForm()

    if form.is_valid():
        for d in all_depts:
            if d['subject'] == form.cleaned_data.get('searched_dept'):
                dept_dict = {}
                dept_dict['subject'] = d['subject']
                # all_depts = []
                # all_depts.append(dept_dict)
                all_depts_search = []
                all_depts_search.append(dept_dict)
                break

    return render(request, 'classlist/class.html', {'form':form, "all_depts_search":all_depts_search, 'a_depts':a_depts, 'b_depts':b_depts, 'c_depts':c_depts, 'd_depts':d_depts, 'e_depts':e_depts, 'f_depts':f_depts, 'g_depts':g_depts, 'h_depts':h_depts, 'i_depts':i_depts, 'j_depts':j_depts, 'k_depts':k_depts, 'l_depts':l_depts, 'm_depts':m_depts, 'n_depts':n_depts, 'o_depts':o_depts, 'p_depts':p_depts, 'q_depts':q_depts, 'r_depts':r_depts, 's_depts':s_depts, 't_depts':t_depts, 'u_depts':u_depts, 'v_depts':v_depts, 'w_depts':w_depts, 'x_depts':x_depts, 'y_depts':y_depts, 'z_depts':z_depts})
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
        # print(course_obj)

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
    """
    https://www.geeksforgeeks.org/how-to-pass-additional-context-into-a-class-based-view-django/
    """
    model = Account
    template_name = 'classlist/view_account.html'
    # extra_context = {"all_friend_requests": Friend_Request.objects.all()}
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context.update({"all_friend_requests": Friend_Request.objects.all()})
        return context

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
        form = UserAccountForm(initial={'USERNAME_FIELD': request.user.username, 'year': "Other", 'major': "Unknown", 'last_login' : timezone.now, 'date_joined' : timezone.now})
        
    return render(request, 'classlist/create_account.html', {'form': form})
    
@login_required
def send_friend_request(request, userID):
    """
    https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
    """
    # template_name = 'classlist/view_account.html'
    # context = {"all_friend_requests": Friend_Request.objects.all()}
    
    user_email = get_user(request).email

    from_user = Account.objects.get(email=user_email)
    to_user = Account.objects.get(id=userID)
    friend_request = Friend_Request(
        from_user = from_user,
        to_user = to_user,
    )
    friend_request.save()

    # return render(request, template_name, context)
    return HttpResponseRedirect('/my_account')

@login_required
def accept_friend_request(request, requestID):
    """
    https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
    """
    # template_name = 'classlist/view_account.html'
    # context = {"all_friend_requests": Friend_Request.objects.all()}

    friend_request = Friend_Request.objects.filter(id=requestID)[0]
    user_email = get_user(request).email
    current_user = Account.objects.filter(email=user_email)[0]

    if friend_request.to_user == current_user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
    else:
        return HttpResponse("Error accepting friend request. Friend request outgoing field did not match current user.")

    # return render(request, template_name, context)
    return HttpResponseRedirect('/my_account')

@login_required
def deny_friend_request(request, requestID):
    """
    https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
    """
    # template_name = 'classlist/view_account.html'
    # context = {"all_friend_requests": Friend_Request.objects.all()}

    friend_request = Friend_Request.objects.get(id=requestID)
    friend_request.delete()

    # return render(request, template_name, context)
    return HttpResponseRedirect('/my_account')

@login_required
def remove_friend(request, requestID):
    
    current_user_email = get_user(request).email
    current_account = Account.objects.filter(email = current_user_email)[0]
    user_friend = Account.objects.get(id=requestID)
    current_account.friends.remove(user_friend)
    user_friend.friends.remove(current_account)

    return redirect('/classlist/my_account/')


def schedule_view(request):
    if request.method == 'POST':
        # s = Schedule() 
        # s.save()         
        # c = request.POST['schedule-button']
        c = request.POST.get('schedule-button')
        if c != None:
            
            mo = False
            if c.find("Mo") != -1:
                mo = True
            
            tu = False
            if c.find("Tu") != -1:
                tu = True

            we = False
            if c.find("We") != -1:
                we = True
            
            th = False
            if c.find("Th") != -1:
                th = True

            fr = False
            if c.find("Fr") != -1:
                fr = True

            sa = False
            if c.find("Sa") != -1:
                sa = True

            su = False
            if c.find("Su") != -1:
                su = True

            schedule_obj = Schedule(course_name = c,
                                    mon = mo,
                                    tue = tu,
                                    wed = we,
                                    thu = th,
                                    fri = fr,
                                    sat = sa,
                                    sun = su
                                    )
            schedule_obj.save()
    added_courses = Schedule.objects.all()
    schedule_context = {'added_courses' : added_courses}
    return render(request, 'classlist/schedule.html', schedule_context)
        # else:
        #     return HttpResponseRedirect('/schedule/')

def delete_course(request):
    if request.method == 'POST':
        # course_id = request.POST['delete-button']
        course_id = int(request.POST.get('delete-button'))
        course = Schedule.objects.get(pk=course_id)
        course.delete()
        # Schedule.objects.all().save()
        # schedule_context = {'added_courses' : added_courses}
    return redirect('schedule')
    # return render(request, 'classlist/schedule.html', schedule_context)

def advanced_search(request):
    template_name = "classlist/advanced_search.html"     

    depts = []
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
    else:
        form = AdvancedSearchForm()

    if form.is_valid():
        dept = form.cleaned_data.get('searched_dept')
        api_url = "http://luthers-list.herokuapp.com/api/dept/" + dept + "/?format=json"
        depts_json = requests.get(api_url)
        depts = depts_json.json()

        depts_search = []  
        for d in depts:
            if d['catalog_number'] not in depts_search:
                depts_search.append(d)
        depts = depts_search
                
    return render(request, "classlist/advanced_search.html" , {'form':form, "depts":depts})


def advanced_search2(request):

    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
    else:
        form = AdvancedSearchForm()
    
    dept_abbr = ""
    all_dept_classes = []
    if form.is_valid():
        dept_abbr = form.cleaned_data.get('searched_dept')
        dept_abbr = dept_abbr.upper()
        api_url = "http://luthers-list.herokuapp.com/api/dept/" + dept_abbr + "/?format=json"
        dept_json = requests.get(api_url)
        all_dept_classes = dept_json.json()
    
    if(Department.objects.filter(dept_abbr=dept_abbr).exists()):
        dept = Department.objects.get(dept_abbr=dept_abbr)
    else:
        dept = Department(dept_abbr=dept_abbr)
        dept.save()

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
        # print(course_obj)

    all_courses = Course.objects.filter(subject = dept_abbr).order_by('department', 'catalog_number')

    if form.is_valid():
        catalog_num = form.cleaned_data.get('searched_catalog_num')
        if catalog_num != None:
            for course in all_courses:
                if course.catalog_number == catalog_num:
                    all_courses = []
                    all_courses.append(course)
    
    if form.is_valid():
        title = form.cleaned_data.get('searched_title')
        if title != None:
            temp = []
            for course in all_courses:
                if title in (course.description).lower():
                    temp.append(course)
            if len(temp) >= 1:
                all_courses = temp


    
    if request.user.is_authenticated:
        dept_context = {"dept" : dept,
                    "dept_abbr" : dept.dept_abbr,
                    "dept_courses" : all_courses,
                    'user' : Account.objects.get(email=request.user.email),
                    "form" : form,
                    }
    else:
        dept_context = {"dept" : dept,
                        "dept_abbr" : dept.dept_abbr,
                        "dept_courses" : all_courses,
                        "form": form,
                        }
         

    return render(request, "classlist/advanced_search.html", context=dept_context)

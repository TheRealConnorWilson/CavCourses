from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView
from urllib3 import HTTPResponse
from .models import Meetings, Instructor, Account, Course, Department, Section, Schedule, Friend_Request, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import UserAccountForm
from .forms import SearchForm, AdvancedSearchForm, CommentForm
from django.db import transaction

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

Title: Aggregating save()s in Django?
URL: https://stackoverflow.com/questions/3395236/aggregating-saves-in-django

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
            'avatar' : account.avatar,
            # 'avatar' : account.avatar,
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

    dept_names = {'ACCT': 'Accounting', 'AIRS': 'Air Science', 'ALAR': 'Architecture and Landscape Architecture', 'AM': 'Applied Mechanics', 'AMST': 'American Studies', 'ANTH': 'Anthropology', 'APMA': 'Applied Mathematics', 
    'ARAB': 'Arabic', 'ARAD': 'Arts Administration', 'ARAH': 'History of Art and Architecture', 'ARCH': 'Architecture', 'ARCY': 'Archaeology', 'ARH': 'Architectural History', 'ARTH': 'History of Art', 'ARTR': 'Arabic in Translation', 'ARTS': 'Studio Art', 
    'ASL': 'American Sign Language', 'ASTR': 'Astronomy', 'BIMS': 'Biomedical Sciences', 'BIOC': 'Biochemistry', 'BIOL': 'Biology', 'BIOP': 'Biophysics', 'BME': 'Biomedical Engineering', 'BUS': 'Business', 'CASS': 'College Art Scholars Seminar', 'CE': 'Civil Engineering', 
    'CELL': 'Cell Biology', 'CHE': 'Chemical Engineering', 'CHEM': 'Chemistry', 'CHIN': 'Chinese', 'CHTR': 'Chinese in Translation', 'CLAS': 'Classics', 'COGS': 'Cognitive Science', 'COLA': 'College Advising Seminar', 'COMM': 'Commerce', 'CONC': 'Concentrations', 'CPE': 'Computer Engineering', 'CREO': 'Creole', 
    'CS': 'Computer Science', 'DANC': 'Dance', 'DEM': 'Democracy', 'DH': 'Digital Humanities', 'DRAM': 'Drama', 'DS': 'Data Science', 'EALC': 'East Asian Languages, Literatures, and Cultures', 'EAST': 'East Asian Studies', 'ECE': 'Electrical and Computer Engineering', 
    'ECON': 'Economics', 'EDHS': 'Education-Human Services', 'EDIS': 'Education-Curriculum, Instruction, & Special Ed', 'EDLF': 'Education-Leadership, Foundations, and Policy', 'EDNC': 'Education Non-Credit', 'EGMT': 'Engagement', 'ELA': 'Engaging the Liberal Arts', 
    'ENCW': 'Creative Writing', 'ENGL': 'English-Literature', 'ENGR': 'Engineering', 'ENTP': 'Entrepreneurship', 'ENWR': 'Writing and Rhetoric', 'ESL': 'English as a Second Language', 'ETP': 'Enviromental Thought and Practice', 'EURS': 'European Studies', 
    'EVAT': 'Environmental Sciences-Atmospheric Sciences', 'EVEC': 'Environmental Sciences-Ecology', 'EVGE': 'Environmental Sciences-Geosciences', 'EVHY': 'Environmental Sciences-Hydrology', 'EVSC': 'Environmental Sciences', 'FREN': 'French', 'GBAC': 'Grad Business Analytics Comm.', 
    'GBUS': 'Graduate Business', 'GCCS': 'Global Commerce in Culture and Society', 'GCNL': 'Clinical Nurse Leader', 'GCOM': 'Graduate Commerce', 'GDS': 'Global Development Studies', 'GERM': 'German', 'GETR': 'German in Translation', 'GHSS': 'Grad Humanities & Social Sci', 'GNUR': 'Graduate Nursing', 
    'GREE': 'Greek', 'GSAS': 'Graduate Arts & Sciences', 'GSCI': 'Graduate Biological and Physical Sciences', 'GSGS': 'Global Studies-Global Studies', 'GSMS': 'GS-Middle East and South Asia', 'GSSJ': 'Global Studies-Security and Justice', 'GSVS': 'Global Studies-Environments and Sustainability', 'HBIO': 'Human Biology', 'HEBR': 
    'Hebrew', 'HHE': 'Health, Humanities & Ethics', 'HIAF': 'History-African History', 'HIEA': 'History-East Asian History', 'HIEU': 'History-European History', 'HILA': 'History-Latin American History', 'HIME': 'History-Middle Eastern History', 'HIND': 'Hindi', 'HISA': 'History-South Asian History', 
    'HIST': 'History-General History', 'HIUS': 'History-United States History', 'HR': 'Human Resources', 'HSCI': 'College Science Scholars Seminar', 'IMP': 'Interdisciplinary Thesis', 'INST': 'Interdisciplinary Studies', 'ISBU': 'Interdisciplinary Studies-Business', 
    'ISHU': 'Interdisiplinary Studies-Humanities', 'ISIN': 'Interdisciplinary Studies-Individualized Other', 'ISLS': 'Interdisciplinary Studies-Liberal Studies Seminar', 'ISSS': 'Interdisciplinary Studies-Social Sciences', 'IT': 'Informational Technology', 
    'ITAL': 'Italian', 'ITTR': 'Italian in Translation', 'JAPN': 'Japanese', 'JPTR': 'Japanese in Translation', 'KICH': "Maya K'iche", 'KINE': 'Kinesiology', 'KLPA': 'Lifetime Physical Activity', 'KOR': 'Korean', 'LAR': 'Landscape Architecture', 
    'LASE': 'Liberal Arts Seminar', 'LAST': 'Latin American Studies', 'LATI': 'Latin', 'LAW': 'Law', 'LING': 'Linguistics', 'LNGS': 'General Linguistics', 'LPPA': 'Leadership and Public Policy - Evaluation and Analysis', 'LPPL': 'Leadership and Public Policy - Leadership', 
    'LPPP': 'Leadership and Public Policy - Policy', 'LPPS': 'Leadership and Public Policy - Substantive', 'MAE': 'Mechanical & Aerospace Engineering', 'MATH': 'Mathematics', 'MDST': 'Media Studies', 'MED': 'Medicine', 
    'MESA': 'Middle Eastern & South Asian Languages & Cultures', 'MICR': 'Microbiology', 'MISC': 'Military Science', 'MSE': 'Materials Science and Engineering', 'MSP': 'Medieval Studies', 'MUBD': 'Music-Marching Band', 'MUEN': 'Music-Ensembles', 
    'MUPF': 'Music-Private Performance Instruction', 'MUSI': 'Music', 'NASC': 'Naval Science', 'NCPR': 'Non-Credit Professional Review', 'NESC': 'Neuroscience', 'NUCO': 'Nursing Core', 'NUIP': 'Nursing Interprofessional', 'NURS': 'Nursing', 'PATH': 'Pathology', 
    'PC': 'Procurement and Contracts Management', 'PERS': 'Persian', 'PETR': 'Persian in Translation', 'PHAR': 'Pharmacology', 'PHIL': 'Philosophy', 'PHS': 'Public Health Sciences', 'PHY': 'Physiology', 'PHYS': 'Physics', 'PLAC': 'Planning Application', 
    'PLAD': 'Politics-Departmental Seminar', 'PLAN': 'Urban and Environmental Planning', 'PLAP': 'Politics-American Politics', 'PLCP': 'Politics-Comparative Politics', 'PLIR': 'Politics-International Relations', 'PLPT': 'Politics-Political Theory', 
    'POL': 'Polish', 'PORT': 'Portuguese', 'POTR': 'Portugese in Translation', 'PPL': 'Political Philosophy, Policy, and Law', 'PSHM': 'PS-Health Sciences Management', 'PSLP': 'PS-Leadership Program', 'PSPA': 'Professional Studies-Public Administration', 
    'PSPM': 'Professional Studies-Project Management', 'PSPS': 'Professional Studies - Public Safety', 'PST': 'Political and Social Thought', 'PSYC': 'Psychology', 'RELA': 'Religion-African Religions', 'RELB': 'Religion-Buddhism', 'RELC': 'Religion-Christianity', 'RELG': 'Religion-General Religion', 
    'RELH': 'Religion-Hinduism', 'RELI': 'Religion-Islam', 'RELJ': 'Religion-Judaism', 'RELS': 'Religion-Special Topic', 'RUSS': 'Russian', 'RUTR': 'Russian in Translation', 'SANS': 'Sanskrit', 'SARC': 'Architecture School', 'SAST': 'South Asian Studies', 
    'SATR': 'South Asian Literature in Translation', 'SEC': 'Cyber Security Analysis', 'SLAV': 'Slavic', 'SLTR': 'Slavic in Translation', 'SOC': 'Sociology', 'SPAN': 'Spanish', 'STAT': 'Statistics', 'STS': 'Science, Technology, and Society', 'SWAH': 'Swahili', 
    'SYS': 'Systems & Information Engineering', 'TURK': 'Turkish', 'UD': 'Urban Design', 'UNST': 'University Studies', 'URDU': 'Urdu', 'USEM': 'University Seminar', 'WGS': 'Women and Gender Studies'}


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
            
    context = {'form':form, "all_depts_search":all_depts_search, 'dept_names':dept_names, 'a_depts':a_depts, 'b_depts':b_depts, 'c_depts':c_depts, 'd_depts':d_depts, 'e_depts':e_depts, 'f_depts':f_depts, 'g_depts':g_depts, 'h_depts':h_depts, 'i_depts':i_depts, 'j_depts':j_depts, 'k_depts':k_depts, 'l_depts':l_depts, 'm_depts':m_depts, 'n_depts':n_depts, 'o_depts':o_depts, 'p_depts':p_depts, 'q_depts':q_depts, 'r_depts':r_depts, 's_depts':s_depts, 't_depts':t_depts, 'u_depts':u_depts, 'v_depts':v_depts, 'w_depts':w_depts, 'x_depts':x_depts, 'y_depts':y_depts, 'z_depts':z_depts}
    
    if request.user.is_authenticated:
        context['user'] = Account.objects.get(email=request.user.email)

    return render(request, 'classlist/class.html', context)
###########

@transaction.atomic
def update_courses_from_API(dept_abbr):
    
    #Access API
    api_url = "http://luthers-list.herokuapp.com/api/dept/" + dept_abbr + "/?format=json"
    dept_json = requests.get(api_url)
    all_dept_classes = dept_json.json()
    
    if(Department.objects.filter(dept_abbr=dept_abbr).exists()):
        dept = Department.objects.get(dept_abbr=dept_abbr)
    else:
        dept = Department(dept_abbr=dept_abbr)
        dept.save()

    #Assign all fields


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
            if meeting_start_time == "":
                meeting_start_time = "00.00.00.000000-05:00"
            meeting_end_time = meeting["end_time"]
            if meeting_end_time == "":
                meeting_end_time = "00.00.00.000000-05:00"
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
            
            # print(course_obj)
            # print(course_obj)
            # setting boolean fields for meetings
            if meetings_obj.days.find("Mo") != -1:
                meetings_obj.monday = True
                # print("Monday")
                # print("Monday")
            if meetings_obj.days.find("Tu") != -1:
                meetings_obj.tuesday = True
                # print("Tuesday")
                # print("Tuesday")
            if meetings_obj.days.find("We") != -1:
                meetings_obj.wednesday = True
                # print("Wednesday")
                # print("Wednesday")
            if meetings_obj.days.find("Th") != -1:
                meetings_obj.thursday = True
                # print("Thursday")
                # print("Thursday")
            if meetings_obj.days.find("Fr") != -1:
                meetings_obj.friday = True
                # print("Friday")
                # print("Friday")
            if meetings_obj.days.find("Sa") != -1:
                meetings_obj.saturday = True
                # print("Friday")
                # print("Friday")
            if meetings_obj.days.find("Su") != -1:
                meetings_obj.sunday = True
                # print("Friday")
                # print("Friday")
                
            # in cases where there are no meetings, none of these will be true (ex. CS 3240's lab section)
            
            
            
            meetings_obj.save()
            
        
        course_obj.save()
        # print(course_obj)



    return dept

@transaction.atomic
def delete_all_courses_from_API():
    Course.objects.all().delete() # delete all of them
    Meetings.objects.all().delete()
    Instructor.objects.all().delete()
    Section.objects.all().delete()
    Schedule.objects.all().delete()
    Department.objects.all().delete()

def load_all_courses_from_API():
    api_url = "http://luthers-list.herokuapp.com/api/deptlist?format=json"
    depts_json = requests.get(api_url)
    all_depts = depts_json.json()

    for dept in all_depts:
        print(dept['subject'])
        update_courses_from_API(dept['subject'])

def load_dept_courses_from_db(request, dept_abbr):
    template_name = "classlist/classes_by_dept.html"

    if Department.objects.filter(dept_abbr = dept_abbr).exists():
        dept = Department.objects.get(dept_abbr = dept_abbr)
        if (timezone.now() - dept.last_updated).days > 7:
            dept = update_courses_from_API(dept_abbr)
    else:
        dept = update_courses_from_API(dept_abbr)

    
    all_dept_courses = Course.objects.filter(subject = dept_abbr).order_by('department', 'catalog_number')

    if request.user.is_authenticated:
        context = {
            "dept": dept,
            "dept_abbr": dept_abbr,
            "dept_courses": all_dept_courses,
            'user': Account.objects.get(email=request.user.email),
        }
    else:
        context = {
            "dept": dept,
            "dept_abbr": dept_abbr,
            "dept_courses": all_dept_courses,
        }

    return render(request, template_name, context)

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
        
        if request.user.socialaccount_set.count() == 0:
            avatar = '/static/classlist/default_account_image.png'
        else:
            avatar = request.user.socialaccount_set.all()[0].get_avatar_url()
            
        new_account = Account(USERNAME_FIELD=request.POST['username'], 
                            email=request.user.email, 
                            first_name=request.user.first_name,
                            last_name=request.user.last_name,
                            date_joined=timezone.now(),
                            is_authenticated=True,
                            major=request.POST['major'],
                            year=request.POST['year'],
                            avatar=avatar
                            )
        new_account.save()
        
        
        schedule_obj = Schedule(scheduleUser=new_account)
        schedule_obj.save()
        
        
        
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


# this method adds to the schedule
def schedule_add(request, section_id):
    # if request.method == 'POST':
        # s = Schedule() 
        # s.save()         
        # c = request.POST['schedule-button']
        # c = request.POST.get('schedule-button')

        # if our post data is valid
        # if c != None:
    if section_id:

        # getting our user
        theUser = Account.objects.filter(USERNAME_FIELD = request.user.username)
        if theUser:
            theUser = theUser[0]
        
        
        sectionToAdd = Section.objects.get(section_id=section_id)
        meetingsToAdd = Meetings.objects.filter(section_id=section_id)

        # if schedule exists, add the class and re-render
        if Schedule.objects.filter(scheduleUser=theUser).exists():
            print("c")

            schedule_obj = Schedule.objects.get(scheduleUser=theUser)

            valid = True

            # courseToAdd = c["section"].course
            

            # if classroster has at least a class in it
            if schedule_obj.classRoster:
                
                time_overlap = False
                conflict = False
                
                # for each class in our schedule, if one isn't compatible, we don't add the class
                for s in schedule_obj.classRoster.all():

                    # need to find associated meeting object with section object
                    meetings = Meetings.objects.filter(section_id=s.section_id)

                    print(meetings)
                    
                    # print(m)
                    
                    # shortcut to check timedate validity - see Activity Scheduling from DSA2
                    # https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
                    for meetingToAdd in meetingsToAdd:

                        for m in meetings:

                            time_overlap = False
                            conflict = False

                            if (meetingToAdd.start_time <= m.end_time) and (m.start_time <= meetingToAdd.end_time):
                                time_overlap = True
                                print("POTENTIAL CONFLICT -- start time:", meetingToAdd, m)
                            
                            elif (m.start_time <= meetingToAdd.end_time) and (meetingToAdd.start_time <= m.end_time):
                                time_overlap = True
                                print("POTENTIAL CONFLICT -- end time:", meetingToAdd, m)
                                
                            #check days overlap as well?
                            
                            if time_overlap: # only need to check if days overlap if time overlaps
                                if m.monday and m.monday == meetingToAdd.monday:
                                    conflict = True
                                    print("POTENTIAL CONFLICT -- monday:", meetingToAdd, m)
                                if m.tuesday and m.tuesday == meetingToAdd.tuesday:
                                    conflict = True
                                    print("POTENTIAL CONFLICT -- tue:", meetingToAdd, m)
                                if m.wednesday and m.wednesday == meetingToAdd.wednesday:
                                    conflict = True
                                    print("POTENTIAL CONFLICT -- wed:", meetingToAdd, m)
                                if m.thursday and m.thursday == meetingToAdd.thursday:
                                    conflict = True
                                    print("POTENTIAL CONFLICT -- thu:", meetingToAdd, m)
                                if m.friday and m.friday == meetingToAdd.friday:
                                    conflict = True
                                    print("POTENTIAL CONFLICT -- fri:", meetingToAdd, m)
                                if m.saturday and m.saturday == meetingToAdd.saturday:
                                    conflict = True
                                    print("POTENTIAL CONFLICT -- sat:", meetingToAdd, m)
                                if m.sunday and m.sunday == meetingToAdd.sunday:
                                    conflict = True
                                    print("POTENTIAL CONFLICT -- sunday:", meetingToAdd, m)
                            

                            if conflict:
                                valid = False
                                print("CONFLICT FOUND:", meetingToAdd, m)
                                break

                # if we can't add class, don't, otherwise do add it
                if valid == False:     
                    print("Cannot add course due to time bounds")       
                else:
                    schedule_obj.classRoster.add(sectionToAdd)
                    print(sectionToAdd)
                    # print(sectionToAdd)
                    schedule_obj.save()

            # if classroster is empty, we can literally just add the class to schedule
            else:
                schedule_obj.classRoster.add(sectionToAdd)
                schedule_obj.save()

            schedule_context = {'the_schedule' : schedule_obj, 'valid' : valid}

            request.session["valid"] = valid

            # return render(request, 'classlist/schedule.html', schedule_context)
            return redirect('/schedule')
            # HttpResponseRedirect(reverse('schedule', kwargs={ 'valid': valid}))
            

            
                
        
        #if schedule does not exists, make one and add the selected course section
        else:
            print("making new schedule")
            # print("making new schedule")

            schedule_obj = Schedule.objects.create(scheduleUser=theUser)

            schedule_obj.classRoster.add(sectionToAdd)
            schedule_obj.save()

            schedule_context = {'the_schedule' : schedule_obj, 'valid': valid}
            print(schedule_obj)
            # print(schedule_obj)
    
            return render(request, 'classlist/schedule.html', schedule_context)

    # if we didn't add anything, go home
    else:
        return HttpResponseRedirect('/home/')

def delete_course(request, section_id):
    # print(section_id)
    if request.method == 'POST':
        # course_id = request.POST['delete-button']

        theUser = Account.objects.filter(USERNAME_FIELD = request.user.username)
        if theUser:
            theUser = theUser[0]

        # sec_id = int(request.POST.get('delete-button'))
        sec_id = section_id
        course = Section.objects.get(section_id=sec_id)

        schedule_obj = Schedule(scheduleUser=theUser)
        schedule_obj.classRoster.remove(course)
        
        # print(schedule_obj.classRoster.all)
        counter = 0
        for each in schedule_obj.classRoster.all():
            print("wow")
            counter += 1
        # if counter == 0:
        #     schedule_obj.delete()
        # else:
        schedule_obj.save()

        schedule_context = {'sched' : schedule_obj}

        # return render(request, 'classlist/schedule.html', schedule_context)
        return redirect('/classlist/schedule/')

def advanced_search2(request):
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
    else:
        form = AdvancedSearchForm()
    
    no_match = False
    dept_abbr = ""
    dept = ""
    all_dept_classes = []
    all_courses = []
    if form.is_valid():
        dept_abbr = form.cleaned_data.get('searched_dept')
        dept_abbr = dept_abbr.upper()
    
    # dept is always required
    if(Department.objects.filter(dept_abbr=dept_abbr).exists()):
        dept = Department.objects.get(dept_abbr=dept_abbr)
    else:
        dept = Department(dept_abbr=dept_abbr)
    
    
    if form.is_valid():
        for course in Course.objects.filter(department=dept):
            all_dept_classes.append(course)
        
        catalog_list = []
        title_list = []
        
        # searches for classes with matching catalog_num (if given)
        catalog_num = form.cleaned_data.get('searched_catalog_num')
        if catalog_num != "":
            for course in Course.objects.filter(department=dept, catalog_number=catalog_num):
                if course.catalog_number == catalog_num:
                    catalog_list.append(course)
        
        # searches for classes with matching title (if given)
        title = form.cleaned_data.get('searched_title')
        if title != "":
            for course in Course.objects.filter(department=dept):
                if title.lower() in (course.description).lower():
                    title_list.append(course)
    
        # generating classes to display
        
        # only dept name given
        if catalog_num == "" and title == "": 
            all_courses = all_dept_classes
        
        # for cases where dept, catalog num exist
        elif catalog_num != "" and title == "": 
            all_courses = catalog_list
    
        # for cases where dept, keyword exist
        elif catalog_num == "" and title != "":
            all_courses = title_list
    
        # for cases where dept, catalog_num, keyword exist
        else:
            # only want the courses that match catalog number and keyword
            for each in catalog_list:
                if title in (each.description).lower():
                    all_courses.append(each)

        if len(all_courses) == 0:
            no_match = True
    
    all_courses.sort()

    if request.user.is_authenticated:
        dept_context = {"dept" : dept,
                    "dept_abbr" : dept.dept_abbr,
                    "dept_courses" : all_courses,
                    'user' : Account.objects.get(email=request.user.email),
                    "no_match" : no_match,
                    "form" : form,
                    }
    else:
        dept_context = {"dept" : dept,
                        "dept_abbr" : dept.dept_abbr,
                        "dept_courses" : all_courses,
                        "no_match" : no_match,
                        "form": form,
                        }
         
    return render(request, "classlist/advanced_search.html", context=dept_context)



def view_comments(request, userID):
    """
    userID: the user who owns the schedule where comments are posted
    """
    
    if userID:
        account = Account.objects.get(id=userID) # whose account the schedule belongs to
        print(account)
        comments_list = Comment.objects.filter(to_user=account)
        print(comments_list)
        
        # my_schedule = Schedule.objects.filter(scheduleUser=account)
    
        context = get_user_info(request)
        # context['my_schedule'] = my_schedule
        context['comments_list'] = comments_list
        
        return render(request, 'classlist/view_comments.html', context)
    else:
        return HTTPResponse("No matching user found")
    
    

def add_comment(request, userID):
    if request.method == 'POST':
        form = CommentForm(request.POST)
    else:
        form = CommentForm()
    
    from_user = Account.objects.get(email=request.user.email)
    to_user = Account.objects.get(id=userID)
    # schedule = Schedule.objects.get(scheduleUser=schedule_owner)
    
    if form.is_valid():
        
        comment_text = form.cleaned_data.get('comment_text')
        if comment_text != "":
            comment = Comment(from_user=from_user, to_user=to_user, text=comment_text)
            comment.save()
            print(comment_text)

    context = get_user_info(request)
    context['from_user'] = from_user
    context['to_user'] = to_user
    # context['schedule'] = schedule
    context['form'] = form
    
    if request.method == 'POST':
        # return render(request, "classlist/schedule.html", context=context)
        return redirect('/classlist/schedule/' + str(to_user.id) + '/')
    else:
        return render(request, "classlist/add_comment.html", context=context)


def schedule_view(request, userID=None):

    time_range = [
        (i*60+2,((str((i - 1) % 12 + 1) if len(str((i - 1) % 12 + 1)) >= 2 
        else ("0" + str((i - 1) % 12 + 1))) 
        + ":00 " + ("AM" if i < 12 else "PM")))
        for i in range(0, 24)]

    weekdays = ["         ", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if userID is None:
        # userID = request.user.email
        if Account.objects.filter(email=request.user.email).exists():
            userID = Account.objects.get(email=request.user.email).id
        else:
            return HttpResponse('No associated schedule found!')

        
    # TODO change to use parameter user instead to make generic
    if Account.objects.filter(id=userID):
        theUser = Account.objects.get(id=userID)

        if not Schedule.objects.filter(scheduleUser=theUser).exists():
            # makes a Schedule for the user if they don't already have one
            schedule_obj = Schedule.objects.create(scheduleUser=theUser)
            schedule_obj.save()

        # if sched exists, pass its context onto schedule template to see it
        if Schedule.objects.filter(scheduleUser=theUser).exists():

            schedule_obj = Schedule.objects.get(scheduleUser=theUser)
            schedule_context = {'the_schedule' : schedule_obj}
            # print(schedule_obj)
            
            meetings_list = []

            for section in schedule_obj.classRoster.all():
                meetings_for_section = Meetings.objects.filter(section=section)
                for meeting in meetings_for_section:
                    meetings_list.append(meeting)
                
            # print(meetings_list)
            # print(meetings_list)
            # print(schedule_obj)
            
            schedule_context['meetings_list'] = meetings_list

            # print(meetings_list)
            # for i in meetings_list:
            #     print(i.y_position())
            #     print(i.length())

            comments_list = Comment.objects.filter(to_user=theUser)
            # print(comments_list)
            # print(comments_list)
        
            
            schedule_context['comments_list'] = comments_list
            schedule_context['user'] = theUser
    
            # find the earliest start time and latest end time
            earliest = 900
            latest = 1700
            other_meetings = []
            for m in meetings_list:

                if m.start_time_as_date_time() == "00:00" and m.end_time_as_date_time() == "00:00": # classes that are "other"
                    other_meetings.append(m)
                
                else:
                    start = int(m.start_time_as_date_time().replace(":", ""))

                    if start < earliest:
                        earliest = start
                    
                    end = int(m.end_time_as_date_time().replace(":", ""))
                    if end > latest:
                        latest = end

            for meeting in other_meetings:
                if meeting in meetings_list:
                    meetings_list.remove(meeting)

            earliest = earliest // 100
            latest = latest // 100
            time_range = time_range[earliest:latest+ 1]
            print(time_range)

            schedule_context['time_range'] = time_range
            schedule_context['weekdays'] = weekdays
            schedule_context['other_meetings'] = other_meetings
            
            return render(request, 'classlist/schedule.html', schedule_context)

    else:
        return render(request, 'classlist/schedule.html', {})
    print("hi")

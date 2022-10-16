from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView

from .models import User, Class

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
   
# first very basic view
class ClassView(generic.ListView):
    template_name = 'classlist/class.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.all()
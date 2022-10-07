from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

"""
Citations:
Title: Python + Django page redirect
URL: https://stackoverflow.com/questions/523356/python-django-page-redirect
"""

#Very basic index page created
def index(request):
    return HttpResponse("Hello, world. You're at the classlist index. Basic Django app created.")
def view_name(request):
    # ex. http://127.0.0.1:8000/accounts/google/login/
    template_name = "classlist/google_login.html"
    return HttpResponseRedirect("/accounts/google/login")
    # model = User # need to make a user model
    
    # options for login page
    # return HttpResponse("This is the login page!")

    # context = {
    #     'user' : user,
    # }
    
    # return render(request, 'google_login.html', context)


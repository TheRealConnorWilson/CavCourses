from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

#Very basic index page created
def index(request):
    return HttpResponse("Hello, world. You're at the classlist index. Basic Django app created.")
def view_name(request):
    return render(request, 'google_login.html', {})
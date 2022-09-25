from django.shortcuts import render
from django.http import HttpResponse

#Very basic index page created
def index(request):
    return HttpResponse("Hello, world. You're at the classlist index. Basic Django app created.")
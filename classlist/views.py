from django.shortcuts import render
from django.http import HttpResponse

#Very basic index page created
def index(request):
    return HttpResponse("This now has a failed test.")
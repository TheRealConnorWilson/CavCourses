from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView

from .models import Class


#Very basic index page created
def index(request):
    return HttpResponse("Hello, world. You're at the classlist index. Basic Django app created.")


# first very basic view
class ClassView(generic.ListView):
    template_name = 'classlist/classes.html'
    context_object_name = 'classes'
    def get_queryset(self):
        return Class.objects.all()



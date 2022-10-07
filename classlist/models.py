from django.db import models
from django.db import models
from django.contrib import admin
# Create your models here.


# first attempt at a model
class Class(models.Model):
    Class_title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    Credits = models.IntegerField()

    def __str__(self):
        return self.Class_title

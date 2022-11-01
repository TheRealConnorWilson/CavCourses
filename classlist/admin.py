from django.contrib import admin

# Register your models here! Otherwise they will not show up in the Admin page
from .models import Account, Instructor, Department, Course, Section, Meetings

admin.site.register(Account)
admin.site.register(Instructor)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Meetings)
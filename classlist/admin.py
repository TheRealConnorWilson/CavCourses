from django.contrib import admin

# Register your models here! Otherwise they will not show up in the Admin page
from .models import Account, Instructor, Department, Course, Section, Meetings, Schedule, Friend_Request, Comment

admin.site.register(Account)
admin.site.register(Instructor)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Meetings)
admin.site.register(Schedule)
admin.site.register(Friend_Request)
admin.site.register(Comment)
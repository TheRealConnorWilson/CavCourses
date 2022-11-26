from django.core.management.base import BaseCommand
from classlist.views import delete_all_courses_from_API
"""
Ciations:

Title: How to Create Custom Django-Admin Commands
URL: https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/
"""

class Command(BaseCommand):
    help = "Deletes all courses in the database, along with Sections, Meetings, etc."

    def handle(self, *args, **options):
        delete_all_courses_from_API()
        self.stdout.write("Courses successfully deleted from DB.")
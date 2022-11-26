from django.core.management.base import BaseCommand
from classlist.views import load_all_courses_from_API
"""
Ciations:

Title: How to Create Custom Django-Admin Commands
URL: https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/
"""

class Command(BaseCommand):
    help = "Manually loads all courses into the DB from the Luther's List API"

    def handle(self, *args, **options):
        load_all_courses_from_API()
        self.stdout.write("Courses successfully loaded into DB.")
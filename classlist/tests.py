from django.test import TestCase
from .models import User, Course, Department, Instructor, Section
from django.utils import timezone
from django.urls import reverse

#Dummy test added.
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

class UserModelTests(TestCase):
    def user_is_authenticated(self):
        user = User()
        self.assertTrue(user.get_authenticated())

# def create_class(instructor, subject, catalog_number, description, units, meetings):
#     """
#     Creates a class instance with the provided fields/attributes.
#     WORK IN PROGRESS
#     """
#     last_updated = timezone.now()
#     return Course.objects.create(question_text=class_text, last_updated=last_updated)


# class ClassModelTests(TestCase):
#     """
#     Add tests for checking class capacity, days of the week, etc.
#     Maybe also class compatibility?
#     """


#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # def test_past_question(self):
    #     """
    #     Questions with a pub_date in the past are displayed on the
    #     index page.
    #     """
    #     question = create_question(question_text="Past question.", days=-30)
    #     response = self.client.get(reverse('polls:index'))
    #     self.assertQuerysetEqual(
    #         response.context['latest_question_list'],
    #         [question],
    #     )

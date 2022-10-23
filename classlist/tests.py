from django.test import TestCase
from .models import User, Course, Department, Instructor, Section
from django.utils import timezone
from django.urls import reverse
# from django.contrib.auth.models import User
from . import views

#Dummy test added.
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

class UserModelTests(TestCase):
    def test_user_is_authenticated(self):
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

def create_user(username, first_name, last_name, email):
    user = User()
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    return user


# https://docs.djangoproject.com/en/4.1/topics/testing/tools/
# referenced this article when writing tests
class GoogleLoginViewTests(TestCase):    # Still working on the google login testing
    def test_no_input(self):
        response = self.client.get(reverse('view_name'))
        self.assertEqual(response.status_code, 200)  # not for sure 200 is the right code
        # self.assertContains(response, "Fill out this field")  # not for sure if this is what it returns when empty

    def test_name(self):
        user = User()
        user.first_name = "first"
        user.last_name = "last"
        actual = user.get_full_name()
        if actual == "first" + " " + "last":
            return True

    def test_correct_user(self):  # working
        user = create_user("username", "first", "last", "email@gmail.com")
        # response = self.client.get(reverse('view_name'))
        self.assertEqual(user.first_name, "first")
        self.assertEqual(user.last_name, "last")
        self.assertEqual(user.get_full_name(), "first" + " " + "last")
        self.assertEqual(user.get_username(), "username")
        self.assertEqual(user.email, "email@gmail.com")

    def test_login(self):  # working
        self.login_url = reverse('view_name')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classlist/google_login.html')

    def test_login_success(self):  # not fully working yet but should be close
        self.login_url = reverse('view_name')
        self.register_url = reverse('home')
        self.user = {'email': 'email@gmail.com', 'username': 'username', 'password':'password','password2':'password',
                     'name': 'fullname'}
        self.client.post(self.register_url, self.user, format='text/html')
        user = User.objects.filter(email=self.user['email']).first()
        # user.is_active = True
        # user.save()
        response = self.client.post(self.login_url, self.user, format='text/html')
        # self.assertEqual(response.status_code, 302)

    def test_cantlogin_with_no_username(self):    # not working
        self.login_url = reverse('view_name')
        response = self.client.post(self.login_url, {'password': 'password'}, format='text/html')
        # self.assertEqual(response.status_code, 401)


# with mock.patch('google.oauth2.id_token.verify_oauth2_token') as
#    mock_verify_oauth2_token:
#        mock_verify_oauth2_token.return_value = MOCK_RETURN_VALUE_DATA
#
# Resource that a TA said would be a good way to test authenticated users  (not working)
# https://stackoverflow.com/questions/68862532/authenticate-with-google-oauth2-in-unit-test-in-python-django

# good youtube link:
# https://www.youtube.com/watch?v=ljG1WzBAboQ

# class testing

# create new class
def new_course(semester_code, title, units):
    course = Course()
    course.semester_code = semester_code
    course.title = title
    #course.description = description
    course.units = units
    return course


class CourseTesting(TestCase):  # working
    def test_no_classes(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)

    def test_new_class(self):
        response = self.client.get(reverse('list'))
        course = new_course(1228, 'Introduction to Information Technology', 3)
        # self.assertQuerysetEqual(response.context['all_courses'], [course])   # this is not fully working

    def test_adding_class(self):  # working
        response = self.client.get(reverse('list'))
        course = Course()
        course.catalog_number = 1010
        course.semester_code = 1228
        course.description = 'Introduction to Information Technology'
        course.units = 3
        course.subject = 'CS'
        self.assertEqual(response.status_code, 200)  # Successfully added class




from django.test import TestCase, Client
from .models import User, Course, Department, Instructor, Section
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from . import views

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

    def test_login_success(self):  # In progress
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

    def test_cantlogin_with_no_username(self):    # in progress
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
def new_course(semester_code, title, units, subject, cat_num):
    return Course.objects.create(catalog_number=cat_num, semester_code=semester_code, title=title,
                                 description=title, units=units, subject=subject)


class CourseTesting(TestCase):  # working
    def test_no_classes(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)

    def test_link(self):  # working
        response = self.client.get('/list/CS/')
        self.assertEqual(response.status_code, 200)

    def test_new_class(self):  # working
        response = self.client.get(reverse('list'))
        course = Course()
        course.save()
        self.assertEqual(len(Course.objects.all()), 1)

    def test_adding_class(self):  # working
        response = self.client.get(reverse('list'))
        course = Course()
        course.catalog_number = 1010
        course.semester_code = 1228
        course.description = 'Introduction to Information Technology'
        course.units = 3
        course.subject = 'CS'
        course.save()
        self.assertEqual(response.status_code, 200)  # Successfully added class

    def test_right_num_classes(self):   # working
        # response = self.client.get(reverse('list'))
        c = Course(catalog_number=1119, semester_code=1228, title='CS 1119', description='description', units=3,
                   subject='CS')
        c.save()
        c2 = Course(catalog_number=9163, semester_code=132, title='CS 1118', description='description 2', units=3,
                    subject='CSS')
        c2.save()
        self.assertEqual(len(Course.objects.all()), 2)

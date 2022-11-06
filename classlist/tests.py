from django.test import RequestFactory, TestCase, Client
from .models import *
from .views import *
from .forms import *
from django.utils import timezone
from django.urls import reverse
# from django.contrib.auth.models import User
from . import views

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

"""
citations:

Testing URL's/Views: talked about it with Riley, our 3240 TA during office hours

Title: django request factory test
URL: https://gist.github.com/dkarchmer/99a35f00503458a4fa3088f5c8215381

"""

#Dummy test added.
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

class AccountModelTests(TestCase):
    def test_user_is_authenticated(self):
        user = Account()
        self.assertTrue(user.get_authenticated())


# def create_class(instructor, subject, catalog_number, description, units, meetings):
#     """
#     Creates a class instance with the provided fields/attributes.
#     WORK IN PROGRESS
#     """
#     last_updated = timezone.now()
#     return Course.objects.create(question_text=class_text, last_updated=last_updated)


def create_user(username, first_name, last_name, email):
    user = Account()
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
        user = Account()
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

    def test_login_success(self):  # in progress
        self.login_url = reverse('view_name')
        self.register_url = reverse('home')
        self.user = {'email': 'email@gmail.com', 'username': 'username', 'password':'password','password2':'password',
                     'name': 'fullname'}
        self.client.post(self.register_url, self.user, format='text/html')
        user = Account.objects.filter(email=self.user['email']).first()
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

client = Client()
class TestViews(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.u1 = User.objects.create_user(username='User1', email='user1@foo.com', password='pass')
        self.a1 = Account(USERNAME_FIELD='User1', email='user1@foo.com', year=2, major='Drama')
        # self.u1.is_active = True
        # self.u1.is_staff = True
        self.u1.save()
        self.a1.save()
        # self.u2 = User.objects.create_user(username='User2', email='user2@foo.com', password='pass')
        # self.a2 = Account.objects.create_user(USERNAME_FIELD='User2', email='user2@foo.com', year=4, major='Computer Engineering')
        # self.u2.is_active = True
        # self.a2.save()
        
    def test_home(self):
        request = self.factory.get('/home')
        request.user = self.u1
        response = view_home(request)
        self.assertEqual(response.status_code, 200)
    
    def test_create_account(self):
        request = self.factory.get('/create_account')
        request.user = self.u1
        response = view_home(request)
        self.assertEqual(response.status_code, 200)
    
    def test_view_departments(self):
        request = self.factory.get('/classlist/list')
        request.user = self.u1
        response = view_home(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_account(self):
        request = self.factory.get('/classlist/my_account')
        request.user = self.u1
        response = view_home(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_CS_department(self):
        request = self.factory.get('/list/CS')
        request.user = self.u1
        response = view_home(request)
        self.assertEqual(response.status_code, 200)

    # def tearDown(self):
    #     Account.objects.all().delete()

    # def setup_request(self, request):
    #     request.user = self.u2

    #     """Annotate a request object with a session"""
    #     middleware = SessionMiddleware()
    #     middleware.process_request(request)
    #     request.session.save()

    #     """Annotate a request object with a messages"""
    #     middleware = MessageMiddleware()
    #     middleware.process_request(request)
    #     request.session.save()

    #     request.session['some'] = 'some'
    #     request.session.save()
    
    # def testGet(self):

    #     url = reverse('some_view')
    #     request = self.factory.get(url)
    #     self.setup_request(request)

    #     view = SomeCreateView.as_view()
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.template_name[0], 'some_template.html')
        
    # def testPost(self):
    #     url = reverse('some_view')+'?arg={0}'.format(self.some.id)
    #     form_data = {
    #         'data1': '1',
    #         'data2': 2
    #     }

    #     request = self.factory.post(url, data=form_data)
    #     self.setup_request(request)

    #     view = SomeCreateView.as_view()
    #     response = view(request)
    #     self.failUnlessEqual(response.status_code, status.HTTP_302_FOUND)
    #     self.assertEqual(SomeModel.objects.count(), 0)  
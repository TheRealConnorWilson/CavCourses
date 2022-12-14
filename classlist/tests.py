from django.test import RequestFactory, TestCase, Client
from .models import *
from .views import *
from .forms import *
from django.utils import timezone
from django.urls import reverse

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
    def initial(self):  # not for sure if this is the proper way to set up
        self.factory = RequestFactory()
        self.user = Account.objects.create_account(USERNAME_FIELD='user', email='email@gmail.com', password='pw')
        self.account = Account.objects.create(email='email@gmial.com')

    def test_no_input(self):
        response = self.client.get(reverse('view_name'))
        self.assertEqual(response.status_code, 200)  # not for sure 200 is the right code

    def test_name(self):
        user = Account()
        user.first_name = "first"
        user.last_name = "last"
        actual = user.get_full_name()
        if actual == "first" + " " + "last":
            return True

    def test_correct_user(self):  # working
        user = create_user("username", "first", "last", "email@gmail.com")
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
        response = self.client.post(self.login_url, self.user, format='text/html')

    def test_cantlogin_with_no_username(self): 
        self.login_url = reverse('view_name')
        response = self.client.post(self.login_url, {'password': 'password'}, format='text/html')

# create new class
def new_course(semester_code, title, units, subject, cat_num):
    return Course.objects.create(catalog_number=cat_num, semester_code=semester_code, title=title,
                                 description=title, units=units, subject=subject)

class CourseTesting(TestCase): 
    def test_home_page(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)

    def test_link(self): 
        response = self.client.get('/list/CS/')
        self.assertEqual(response.status_code, 200)

    def test_accounts(self):
        response = self.client.get('/list/accounts/')
        self.assertEqual(response.status_code, 200)

    def test_my_account(self):
        response = self.client.get('/list/my_account/')
        self.assertEqual(response.status_code, 200)

    def test_view_users(self):
        response = self.client.get('/list/view_users/')
        self.assertEqual(response.status_code, 200)

    def test_create_account(self):
        response = self.client.get('/create_account/')
        self.assertEqual(response.status_code, 200)

    def advanced_search(self): 
        response = self.client.get('/advanced_search/')
        self.assertEqual(response.status_code, 200)

    def my_account_link(self):
        response = self.client.get('/my_account/')
        self.assertEqual(response.status_code, 200)

    def test_new_class(self):
        response = self.client.get(reverse('list'))
        course = Course()
        course.save()
        self.assertEqual(len(Course.objects.all()), 1)

    def test_adding_class(self):
        response = self.client.get(reverse('list'))
        course = Course()
        course.catalog_number = 1010
        course.semester_code = 1228
        course.description = 'Introduction to Information Technology'
        course.units = 3
        course.subject = 'CS'
        course.save()
        self.assertEqual(response.status_code, 200) 

    def test_right_num_classes(self): 
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
        self.factory = RequestFactory()
        self.u1 = User.objects.create_user(username='User1', email='user1@foo.com', password='pass')
        self.a1 = Account(USERNAME_FIELD='User1', email='user1@foo.com', year=2, major='Drama')
        self.s1 = Schedule(scheduleUser=self.a1)
        self.u1.save()
        self.a1.save()
        self.s1.save()
        
        
        self.u2 = User.objects.create_user(username='User2', email='user2@foo.com', password='pass')
        self.a2 = Account(USERNAME_FIELD='User2', email='user2@foo.com', year=1, major='Undeclared')
        self.s2 = Schedule(scheduleUser=self.a2)
        self.u2.save()
        self.a2.save()
        self.s2.save()
        
    def test_home(self):
        request = self.factory.get('/home')
        request.user = self.u1
        response = view_home(request)
        self.assertEqual(response.status_code, 200)
    
    def test_create_account(self):
        request = self.factory.get('/create_account')
        request.user = self.u1
        response = create_account(request)
        self.assertEqual(response.status_code, 200)
    
    def test_view_departments(self):
        request = self.factory.get('/classlist/list')
        request.user = self.u1
        response = get_depts(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_account(self):
        request = self.factory.get('/classlist/my_account')
        request.user = self.u1
        response = ViewAccount.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_CS_department(self):
        request = self.factory.get('/list/CS')
        request.user = self.u1
        response = load_dept_courses_from_db(request, 'CS')
        self.assertEqual(response.status_code, 200)
        
    def test_view_my_schedule(self):
        request = self.factory.get('/classlist/schedule/')
        request.user = self.u1
        response = schedule_view(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_users(self):
        request = self.factory.get('/classlist/account/view_users')
        request.user = self.u1
        response = ViewUsers.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_other_schedule(self):
        request = self.factory.get('/classlist/schedule/' + str(self.u2.id))
        request.user = self.u1
        response = schedule_view(request, self.u2.id)
        self.assertEqual(response.status_code, 200)
        
    def test_add_comment(self):
        request = self.factory.get('/classlist/schedule/' + str(self.u2.id) +'/add_comment')
        request.user = self.u1
        response = add_comment(request, self.u2.id)
        self.assertEqual(response.status_code, 200)

class FriendsFeaturesTesting(TestCase):
    def test_friends(self):
        account = Account(USERNAME_FIELD='account', email='account@email.com')
        account.save()
        account2 = Account(USERNAME_FIELD='account2', email='account2@email.com')
        account2.save()
        response = self.client.get(reverse('my_account'))
        self.assertEqual(len(Account.objects.all()), 2)
        self.assertEqual(response.status_code, 200)


class TestSchedule(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.u1 = User.objects.create_user(username='User1', email='user1@foo.com', password='pass')
        self.a1 = Account(USERNAME_FIELD='User1', email='user1@foo.com', year=2, major='Drama')
        self.u1.save()
        self.a1.save()

    def test_no_schedule(self):
        request = self.factory.get('/classlist/schedule/')
        request.user = self.u1
        response = schedule_view(request)
        self.assertEqual(len(Schedule.objects.all()), 1) # tweaked because now a Schedule will be created to be displayed (avoid error)

    def test_create_schedule(self):
        schedule_obj = Schedule(scheduleUser=self.a1)
        schedule_obj.save()
        self.assertEqual(len(Schedule.objects.all()), 1)


class FriendsFeaturesTesting(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.u1 = User.objects.create_user(username='User1', email='user1@foo.com', password='pass')
        self.a1 = Account(USERNAME_FIELD='User1', email='user1@foo.com', year=2, major='Drama')
        self.u1.save()
        self.a1.save()

    def test_friends(self):

        request = self.factory.get('/classlist/my_account/')
        request.user = self.u1
        response = ViewAccount.as_view()(request)

        account = Account(USERNAME_FIELD='account', email='account@email.com')
        account.save()
        account2 = Account(USERNAME_FIELD='account2', email='account2@email.com')
        account2.save()
        self.assertEqual(len(Account.objects.all()), 3)
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        request = self.factory.get('/classlist/view_users/')
        request.user = self.u1
        response = ViewUsers.as_view()(request)
        account = Account(USERNAME_FIELD='account', email='account@email.com')
        account.save()
        account2 = Account(USERNAME_FIELD='account2', email='account2@email.com')
        account2.save()
        self.assertEqual(response.status_code, 200)


class AdvancedSearchTesting(TestCase):
    def test_search(self):
        response = self.client.get(reverse('advanced_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('classlist/advanced_search.html')


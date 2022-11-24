from django.test import RequestFactory, TestCase, Client
from .models import *
from .views import *
from .forms import *
from django.utils import timezone
from django.urls import reverse
# from django.contrib.auth.models import User
# from . import views
#
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.contrib.messages.middleware import MessageMiddleware
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

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
    def initial(self):  # not for sure if this is the proper way to set up
        self.factory = RequestFactory()
        self.user = Account.objects.create_account(USERNAME_FIELD='user', email='email@gmail.com', password='pw')
        self.account = Account.objects.create(email='email@gmial.com')

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
    def test_home_page(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)

    def test_link(self):  # working
        response = self.client.get('/list/CS/')
        self.assertEqual(response.status_code, 200)

    def test_accounts(self):  # working
        response = self.client.get('/list/accounts/')
        self.assertEqual(response.status_code, 200)

    def test_my_account(self):  # working
        response = self.client.get('/list/my_account/')
        self.assertEqual(response.status_code, 200)

    def test_view_users(self):  # working
        response = self.client.get('/list/view_users/')
        self.assertEqual(response.status_code, 200)

    def test_create_account(self):  # working
        response = self.client.get('/create_account/')
        self.assertEqual(response.status_code, 200)

    def advanced_search(self):  # working
        response = self.client.get('/advanced_search/')
        self.assertEqual(response.status_code, 200)

    def my_account_link(self):  # working
        response = self.client.get('/my_account/')
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
        self.s1 = Schedule(scheduleUser=self.a1)
        # self.u1.is_active = True
        # self.u1.is_staff = True
        self.u1.save()
        self.a1.save()
        self.s1.save()
        
        
        self.u2 = User.objects.create_user(username='User2', email='user2@foo.com', password='pass')
        self.a2 = Account(USERNAME_FIELD='User2', email='user2@foo.com', year=1, major='Undeclared')
        self.s2 = Schedule(scheduleUser=self.a2)
        # self.u1.is_active = True
        # self.u1.is_staff = True
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

# https://selenium-python.readthedocs.io/getting-started.html#using-selenium-to-write-tests
# good testing link


# class SeleniumTests(TestCase):  # this could definitely cause problems for people
#     # must install selenium and download chrome driver from https://sites.google.com/chromium.org/driver/
#     # good video that I used for help https://www.youtube.com/watch?v=1KbJdhIpcGo
#     # main documentation for selenium https://selenium-python.readthedocs.io/index.html
#     # after installing the chrome webdriver, move it to the bin folder in your virtual environment folder
#     #drive = webdriver.Chrome(executable_path='../env/chromedriver')
#     #drive.get('https://a27-lous-list.herokuapp.com/view_users/')
#     # elem1 = drive.find_element(By.LINK_TEXT, "Login")
#     # elem1.click()
#     # elem3 = drive.find_element(By.ID, "identifierId")
#     # elem3.send_keys('nth5pdk@virginia.edu')
#     # elem3.send_keys(Keys.RETURN)
#     # elem4 = drive.find_element(By.ID, 'certLogin')
#     # elem4.click()
#     # elem5 = drive.find_element(By.LINK_TEXT, 'OK')
#     # elem5.click()
#     # elem = drive.find_element(By.LINK_TEXT, "My_Account")
#     # elem.click()
#     # elem2 = drive.find_element(By.LINK_TEXT, "Find Friends")
#     # elem2.click()
#     # element = drive.find_element(By.LINK_TEXT, "View all ACCT classes")
#     # element.click()
#     #elem2 = drive.find_element(By.LINK_TEXT, "Continue")
#     #elem2.click()
#     #elem = drive.find_element(By.NAME, 'searched_dept')
#     #elem.send_keys('CS')
#     #elem.send_keys(Keys.RETURN)
#     #print(drive.page_source)
#     # elem = drive.find_element(By.LINK_TEXT, "View all ACCT classes")
#     # elem.click()
#     # print(elem.__class__)
#     def clicking_home_from_class(self):
#         driver1 = self.driver
#         driver1.get('https://a27-lous-list.herokuapp.com/list/')
#         elem3 = driver1.find_element(By.LINK_TEXT, "View all ACCT classes")
#         elem3.click()
#         elem1 = driver1.find_element(By.LINK_TEXT, "Home")
#         elem1.click()
#         self.assertIn("Departmentsssss", driver1.page_source)
#
#     def clicking_login(self):
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/list/')
#         elem2 = driver3.find_element(By.LINK_TEXT, "Login")
#         elem2.click()
#         self.assertIn("Sign In Via Google", driver3.page_source)
#
#     def test_clicking_classes(self):  # verifies that clicking on a course card will take you to all the sections (good)
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/list/')
#         self.assertIn('', driver3.title)
#         elem = driver3.find_element(By.LINK_TEXT, "View all ACCT classes")
#         elem.click()
#         #self.assertIn("Section Information", driver3.page_source)
#         #self.assertIn("ACCT Classes", driver3.page_source)
#         #self.assertIn("ACCT 2010", driver3.page_source)
#
#     def test_search_class(self):
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/advanced_search/')
#         self.assertIn('', driver3.title)
#         elem = driver3.find_element(By.NAME, 'searched_dept')
#         elem.send_keys('CS')
#         elem.send_keys(Keys.RETURN)
#         self.assertIn("Introduction to Programming", driver3.page_source)
#
#     def test_logging_in(self):  # verifies that clicking on a course card will take you to all the sections (good)
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/')
#         elem = driver3.find_element(By.LINK_TEXT, "Login")
#         elem.click()
#         # elem2 = driver3.find_element(By.LINK_TEXT, "Continue")
#         # elem2.click()
#         # self.assertIn("Sign In Via Google", driver3.page_source)
#
#     def test_apma_class(self):  # verifies that clicking on a course card will take you to all the sections (good)
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/list/')
#         element = driver3.find_element(By.LINK_TEXT, "View all APMA classes")
#         element.click()
#         #element2 = driver3.find_element(By.LINK_TEXT, "Departments")
#         #element2.click()
#         #element3 = driver3.find_element(By.__class__, "btn btn-secondary collapsed")
#         #self.assertIn("Search for a department", driver3.page_source)
#
#     def search_class(self):
#         # self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver = self.driver
#         driver.get('https://a27-lous-list.herokuapp.com/advanced_search/')
#         elem = driver.find_element(By.NAME, 'searched_dept')
#         elem.send_keys('cs')
#         elem.send_keys(Keys.RETURN)
#         self.assertIn("Introduction to Programming", driver.page_source)
#
#     # def test_schedule_builder(self):  # verifies that clicking on a course card will take you to all the sections (good)
#     #     self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#     #     driver3 = self.driver
#     #     driver3.get('https://a27-lous-list.herokuapp.com/list/')
#     #     elem = driver3.find_element(By.LINK_TEXT, "Schedule Builder")
#     #     elem.click()
#     #     self.assertIn("My Schedule", driver3.page_source)
#
#     def test_advanced_search(self):
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/classlist/advanced_search/')
#         elem = driver3.find_element(By.NAME, "searched_dept")
#         elem.send_keys('CS')
#         elem2 = driver3.find_element(By.NAME, "searched_catalog_num")
#         elem2.send_keys('4414')
#         elem2.send_keys(Keys.RETURN)
#         self.assertIn("Operating Systems", driver3.page_source)
#
#     def test_advanced_search2(self):
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/classlist/advanced_search/')
#         elem = driver3.find_element(By.NAME, "searched_dept")
#         elem.send_keys('ece')
#         elem2 = driver3.find_element(By.NAME, "searched_title")
#         elem2.send_keys('fundamentals')
#         elem2.send_keys(Keys.RETURN)
#         self.assertIn("ECE Fundamentals I", driver3.page_source)
#
#     # def test_my_account(self):
#     #     self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#     #     driver3 = self.driver
#     #     driver3.get('https://a27-lous-list.herokuapp.com/classlist/list/')
#     #     elem1 = driver3.find_element(By.LINK_TEXT, "Login")
#     #     elem1.click()
#     #     elem3 = driver3.find_element(By.ID, "identifierId")
#     #     elem3.send_keys('nth5pdk@virginia.edu')
#     #     elem3.send_keys(Keys.RETURN)
#     #     elem = driver3.find_element(By.LINK_TEXT, "My_Account")
#     #     elem.click()
#     #     elem2 = driver3.find_element(By.LINK_TEXT, "Find Friends")
#     #     elem2.click()
#     #     elem4 = driver3.find_element(By.ID, 'certLogin')
#     #     elem4.click()
#     #     elem5 = driver3.find_element(By.LINK_TEXT, 'OK')
#     #     elem5.click()
#     #     elem = driver3.find_element(By.LINK_TEXT, "My_Account")
#     #     elem.click()
#     #     elem2 = driver3.find_element(By.LINK_TEXT, "Find Friends")
#     #     elem2.click()
#     #     self.assertIn("Other Users", driver3.page_source)
#
#     def test_other_users(self):
#         self.driver = webdriver.Chrome(executable_path='../env/bin/chromedriver')
#         driver3 = self.driver
#         driver3.get('https://a27-lous-list.herokuapp.com/view_users/')
#         self.assertIn("Send friend request", driver3.page_source)
#
#
#     def tearDown(self):
#         self.driver.close()

class FriendsFeaturesTesting(TestCase):
    def test_friends(self):
        response = self.client.get(reverse('my_account'))
        account = Account(USERNAME_FIELD='account', email='account@email.com')
        account.save()
        account2 = Account(USERNAME_FIELD='account2', email='account2@email.com')
        account2.save()
        self.assertEqual(len(Account.objects.all()), 2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classlist/view_account.html')

        #req = Friend_Request(from_user=account)
        # rec = Friend_Request(to_user=account2)
        # account.friends.add(rec)


class TestSchedule(TestCase):  # Johnny's Tests

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.u1 = User.objects.create_user(username='User1', email='user1@foo.com', password='pass')
        self.a1 = Account(USERNAME_FIELD='User1', email='user1@foo.com', year=2, major='Drama')
        # self.s1 = Schedule(scheduleUser=self.a1)
        # self.u1.is_active = True
        # self.u1.is_staff = True
        self.u1.save()
        self.a1.save()
        # self.s1.save()

    # if we have no schedule, create one - now test it
    def test_no_schedule(self):
        request = self.factory.get('/classlist/schedule/')
        request.user = self.u1
        response = schedule_view(request)
        self.assertEqual(len(Schedule.objects.all()), 0)

    def test_create_schedule(self):
        schedule_obj = Schedule(scheduleUser=self.a1)
        schedule_obj.save()
        self.assertEqual(len(Schedule.objects.all()), 1)



class FriendsFeaturesTesting(TestCase):
    def test_friends(self):
        response = self.client.get(reverse('my_account'))
        account = Account(USERNAME_FIELD='account', email='account@email.com')
        account.save()
        account2 = Account(USERNAME_FIELD='account2', email='account2@email.com')
        account2.save()
        self.assertEqual(len(Account.objects.all()), 2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classlist/view_account.html')

        #req = Friend_Request(from_user=account)
        # rec = Friend_Request(to_user=account2)
        # account.friends.add(rec)

    def test_users(self):
        response = self.client.get(reverse('view_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classlist/view_users.html')


class AdvancedSearchTesting(TestCase):
    def test_search(self):
        response = self.client.get(reverse('advanced_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('classlist/advanced_search.html')


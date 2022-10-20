from django.test import TestCase
from .models import User
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


def create_user(username, first_name, last_name, email):
    user = User()
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    return user


# https://docs.djangoproject.com/en/4.1/topics/testing/tools/
# referenced this article when writing tests
class GoogleLoginViewTests(TestCase):
    def test_no_input(self):
        response = self.client.get(reverse('view_name'))
        self.assertEqual(response.status_code, 200)  # not for sure 200 is the right code
        #self.assertContains(response, "Fill out this field")  # not for sure if this is what it returns when empty

    def test_name(self):  # next test basically covers all this, but I'm going to leave it here anyway.
        user = User()
        user.first_name = "first"
        user.last_name = "last"
        actual = user.get_full_name()
        if actual == "first" + " " + "last":
            return True

    def test_correct_user(self):
        user = create_user("username", "first", "last", "email@gmail.com")
        #response = self.client.get(reverse('view_name'))
        self.assertEqual(user.first_name, "first")
        self.assertEqual(user.last_name, "last")
        self.assertEqual(user.get_full_name(), "first" + " " + "last")
        self.assertEqual(user.get_username(), "username")
        self.assertEqual(user.email, "email@gmail.com")


# class LoginTestCase(TestCase):
    # def test_login(self):
        # response = self.client.get('/classlist/login')
        # self.assertRedirects(response, '/classlist/accounts/login/')

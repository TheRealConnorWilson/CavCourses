from django.test import TestCase
from .models import User

#Dummy test added.
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 2)

class UserModelTests(TestCase):
    def user_is_authenticated(self):
        user = User()
        self.assertTrue(user.get_authenticated())
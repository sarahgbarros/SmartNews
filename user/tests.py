from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="gabi", password="123456")
        self.assertEqual(user.username, "gabi")
        self.assertTrue(user.check_password("123456"))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        
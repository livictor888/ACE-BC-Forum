from django.test import TestCase
from django.contrib.auth import get_user_model


class URLTests(TestCase):
        # Test creating a user
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12te12', email='test@example.com')
        self.user.save()

    def test_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        response = self.client.get('/password-reset')
        self.assertEqual(response.status_code, 301)


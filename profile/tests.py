from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

class URLTests(TestCase):
    # Create a user
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='test', password='12te12', email='test@example.com')
        self.user.save()

    # Test valid url
    def test_profile_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_profile__edit_page(self):
        response = self.client.get('/profile/edit')
        self.assertEqual(response.status_code, 200)
    
     # Test invalid url
    def test_invalid_profile_edit_page(self):
        response = self.client.get('/edit')
        self.assertEqual(response.status_code, 404)

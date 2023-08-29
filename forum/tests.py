from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from .views import PostCreate
from .models import Post

class URLTests(TestCase):
    # Create a user
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12te12', email='test@example.com')
        self.user.save()

    # Test valid url
    def test_testhomepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_forum(self):
        response = self.client.get('/forum')
        self.assertEqual(response.status_code, 301)

    def test_forum_new(self):
        response = self.client.get('/forum/new')
        self.assertEqual(response.status_code, 301)

    def test_forum_search(self):
        response = self.client.get('/forum/new')
        self.assertEqual(response.status_code, 301)

    def test_year_search(self):
        response = self.client.get('/forum/year')
        self.assertEqual(response.status_code, 301)
    

    def test_search(self):
        response = self.client.get('/forum/search')
        self.assertEqual(response.status_code, 301)
    

    # Test invalid url 
    def test_invalid_year_search(self):
        response = self.client.get('/year')
        self.assertEqual(response.status_code, 404)

    def test_invalid_post(self):
        response = self.client.get('/list')
        self.assertEqual(response.status_code, 404)


class ForumPageTest(TestCase):
    """ Test create post page"""
    def test_view_set_in_context_create_post(self):
        request = RequestFactory().get('/forum/new')
        view = PostCreate()
        view.setup(request)

        context = view.get_context_data()
        
        self.assertIn('view', context)


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Post1", body="This is post 1")
        Post.objects.create(title="Post2", body="This is post 2")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        post1 = Post.objects.get(title="Post1")
        post2 = Post.objects.get(title="Post2")
        self.assertEqual(post1.body, "This is post 1")
        self.assertEqual(post2.body, "This is post 2")

    
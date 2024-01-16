from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from blog_app.models import *
from api.serializers import *


class PostViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name='testfirstname',
                                        last_name='testlastname',
                                        email='testemail@gmail.com'
                                        ,username='testuser', password='testpass')
        self.category = Category.objects.create(text='testcategory', author=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {
            "title": "Test Post",
            "body": "This is a test post.",
            "author": self.user,
            "description": "Test post description",
            "category": self.category
        }
        response = self.client.post('/api/posts/', data)
        print('----------------------------------------------------------------------')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)  # Check if 'id' is present in the response
        # Add more assertions as needed

    def test_get_post_list(self):
        response = self.client.get('/api/posts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Check if the response contains posts
        # Add more assertions as needed

    def test_get_single_post(self):
        post = Post.objects.create(title="Test Post", body="This is a test post.", author=self.user, slug='test-post')
        print(self.client.get(f'/posts/{post.slug}'))
        response = self.client.get(f'/api/posts/{post.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Post")
        # Add more assertions as needed


# ادامه تست‌ها برای بخش‌های دیگر ویوها

class PostSerializerTests(TestCase):
    def test_valid_post_serializer(self):
        data = {
            "title": "Test Post",
            "body": "This is a test post.",
            "description": "Test post description",
            "author": "admin",
            "category": "programming language"
        }
        serializer = PostCreateUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_post_serializer(self):
        data = {
            "title": "",
            "body": "This is a test post.",
            "description": "Test post description",
            "author": "admn",
            "category": "programming laguage"
        }
        serializer = PostCreateUpdateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # Add more assertions as needed



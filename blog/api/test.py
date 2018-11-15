from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

from blog.models import Blog

User = get_user_model()


class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username="khan", email="me.khan@khanwork.com")
        user_obj.set_password("some_random_password")
        user_obj.save()
        blog_post = Blog.objects.create(user=user_obj, title="whatever title", content="whatever content")

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = User.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("post-list")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list(self):
        data = {"title": "random title", "content": "random content"}
        url = api_reverse("post-list")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog_post = Blog.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        blog_post = Blog.objects.first()
        data = {"title": "random title", "content": "random content"}
        url = blog_post.get_api_url()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

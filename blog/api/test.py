from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

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

    def test_update_item_with_user(self):
        blog_post = Blog.objects.first()
        data = {"title": "random title", "content": "random content"}
        url = blog_post.get_api_url()
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZED='JWT ' + token_rsp)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_item_with_user(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {"title": "random title", "content": "random content"}
        url = api_reverse("post-list")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='abdullah')
        blog_post = Blog.objects.create(user=owner, title="whatever title", content="whatever content")

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)

        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data = {"title": "random title", "content": "random content"}
        url = blog_post.get_api_url()

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': 'khan',
            'password': 'some_random_password'
        }
        url = api_reverse('api-login')
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            blog_post = Blog.objects.first()
            data = {"title": "random title", "content": "random content"}
            url = blog_post.get_api_url()
            self.client.credentials(HTTP_AUTHORIZED='JWT ' + token)

            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

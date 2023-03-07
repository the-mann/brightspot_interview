from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import BlogPost


class BlogPostTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('admin', password="admin")
        self.user.save()

        # Create blogpost owned by user
        self.example_blogpost = BlogPost.objects.create(title="title", subtitle="sub", body="bod", owner=self.user)
        self.example_blogpost.save()

    def tearDown(self) -> None:
        self.client.logout()

    def test_403_on_unauthenticated_create_blogpost(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('blogpost-list')
        data = {
            "title": "title",
            "subtitle": "sub",
            "body": "bod"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_200_on_authenticated_create_blogpost(self):
        """
        Ensure we can create a new account object.
        """
        # generate new Django user for testing
        url = reverse('blogpost-list')
        data = {
            "title": "title",
            "subtitle": "sub",
            "body": "bod"
        }
        self.client.login(username='admin', password='admin')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)

    def test_unauthenticated_can_read_blogspot(self):
        blogpost = BlogPost.objects.create(title="title", subtitle="sub", body="bod", owner=self.user)
        blogpost.save()
        url = reverse('blogpost-detail', args=[blogpost.id])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], blogpost.id)

    def test_get_blogposts_of_user(self):
        self.assertTrue(len(self.user.blogposts.all()) > 0)
        self.assertEqual(self.user.blogposts.first(), self.example_blogpost)

from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from udigital import settings
from udigital.models import PhoneNumber, User, Post

settings.USE_TEST_MIDDLEWARE = False


class UDigitalViewsTest(TestCase):

    def setUp(self):
        self.phone_number = PhoneNumber.objects.create(number='911333444', dial_code='+421')
        self.user = User.objects.create(first_name='Anonymous', last_name='User', email='anonymous@user.com',
                                        phone_number=self.phone_number)
        self.post = Post.objects.create(title='Test', content='Test', author=self.user, publication_date=datetime.now())

    def test_post_list_view(self):
        url = reverse('list_posts_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['author']['first_name'], 'Anonymous')
        self.assertEqual(response.data[0]['author']['last_name'], 'User')
        self.assertEqual(response.data[0]['title'], 'Test')

    def test_post_detail_view(self):
        url = reverse('post_detail_view', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['author']['first_name'], 'Anonymous')
        self.assertEqual(response.data['author']['last_name'], 'User')
        self.assertEqual(response.data['content'], 'Test')
        self.assertEqual(response.data['title'], 'Test')

    def test_post_create_view(self):
        url = reverse('post_create_view')
        data = {
            'title': 'Test',
            'content': 'Test',
            'author_id': 1,
            'publication_date': '2021-05-05'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_comment_create_view(self):
        url = reverse('comment_create_view')
        data = {
            'post_id': 1,
            'user_id': 1,
            'comment': 'Cool'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

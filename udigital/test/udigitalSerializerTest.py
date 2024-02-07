from datetime import datetime

from django.test import TestCase

from udigital.models import User, Post, PhoneNumber
from udigital.serializer import UserSerializer, CommentSerializer, PostListSerializer, PostDetailSerializer, \
    PostCreateSerializer, CommentCreateSerializer


class UDigitalSerializerTest(TestCase):

    def setUp(self):
        self.phone_number = PhoneNumber.objects.create(number='911222333', dial_code='+421')
        self.user = User.objects.create(first_name='Anonymous', last_name='User', email='anonymous@user.com', phone_number=self.phone_number)
        self.post = Post.objects.create(title='Test', content='Test', author=self.user, publication_date=datetime.now())

    def test_user_serializer(self):
        serializer = UserSerializer({'first_name': 'John', 'last_name': 'Doe'})
        data = serializer.data
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')

    def test_comment_serializer(self):
        serializer = CommentSerializer({'comment': 'Cool', 'user': {'first_name': 'John', 'last_name': 'Doe'}})
        data = serializer.data
        self.assertEqual(data['comment'], 'Cool')
        self.assertEqual(data['user']['first_name'], 'John')
        self.assertEqual(data['user']['last_name'], 'Doe')

    def test_post_list_serializer(self):
        serializer = PostListSerializer(
            [{'id': 1, 'title': 'World of warcraft', 'author': {'first_name': 'John', 'last_name': 'Doe'}, 'content': 'Test', 'publication_date': '2021-05-05'}],
            many=True)
        data = serializer.data
        self.assertEqual(data[0]['title'], 'World of warcraft')
        self.assertEqual(data[0]['author']['first_name'], 'John')
        self.assertEqual(data[0]['author']['last_name'], 'Doe')

    def test_post_detail_serializer(self):
        serializer = PostDetailSerializer(
            {'id': 1, 'title': 'World of warcraft', 'author': {'first_name': 'John', 'last_name': 'Doe'}, 'content': 'Test', 'publication_date': '2021-05-05'})
        data = serializer.data
        self.assertEqual(data['title'], 'World of warcraft')
        self.assertEqual(data['author']['first_name'], 'John')
        self.assertEqual(data['author']['last_name'], 'Doe')
        self.assertEqual(data['content'], 'Test')

    def test_post_create_serializer(self):
        serializer = PostCreateSerializer(data={'title': 'World', 'author_id': 1, 'content': 'Hello World!', 'publication_date': '2022-01-01'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        self.assertEqual(data['title'], 'World')
        self.assertEqual(data['content'], 'Hello World!')
        self.assertEqual(data['publication_date'], '2022-01-01')

    def test_comment_create_serializer(self):
        serializer = CommentCreateSerializer(data={'post_id': 1, 'user_id': 1, 'comment': 'Cool'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        self.assertEqual(data['comment'], 'Cool')

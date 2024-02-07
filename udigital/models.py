from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

SUPER_ADMIN = 1


class PhoneNumber(models.Model):
    id = models.AutoField(primary_key=True)
    dial_code = models.CharField(max_length=5, default='+421')
    country_code = models.CharField(max_length=2, default='SK')
    number = models.CharField(max_length=15)

    REQUIRED_FIELDS = ['dial_code', 'country_code', 'number']

    def delete(self, *args, **kwargs):
        raise Exception("You cannot delete this object.")

    def __str__(self):
        return '{} - {}'.format(self.dial_code, self.number)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email, password, **extra_fields)

        group = Group.objects.get(pk=SUPER_ADMIN)
        user.groups.add(group)

        return user


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.PROTECT)
    password = models.CharField(max_length=20, default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    def delete(self, *args, **kwargs):
        raise Exception("You cannot delete this object.")

    def __str__(self):
        return '{} {} - {}'.format(self.first_name, self.last_name, self.email)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    publication_date = models.DateField()

    REQUIRED_FIELDS = ['title', 'content', 'author', 'publication_date']

    def __str__(self):
        return '{} - {}'.format(self.title, self.author)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # TODO: Split to created comment and updated comment
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='comments')
    comment = models.TextField()

    REQUIRED_FIELDS = ['user', 'post', 'comment']

    def __str__(self):
        return '{} - {}'.format(self.post, self.user)

from django.db import models
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    return 'user_{0}/profile/{1}'.format(instance.user.id, filename)


class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_directory_path, null=True, default='default.png')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

    def to_json(self):
        return {
            'last_login': self.last_login,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_active': self.is_active,
            'avatar': str(self.avatar),
            'bio': self.bio,
        }

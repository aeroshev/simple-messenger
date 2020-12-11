from django.db import models
from users.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/chat/{1}'.format(instance.creator.id, filename)


class Chat(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False, default='NoName')
    is_group_chat = models.BooleanField(null=False, blank=False, default=False)
    chat_avatar = models.ImageField(upload_to=user_directory_path,
                                    null=False, blank=False, default='default/default.png')
    last_message = models.OneToOneField('message.Message', on_delete=models.SET_NULL, null=True, related_name='Chat')
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'title ' + self.title

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'is_group_chat': self.is_group_chat,
            'chat_avatar': str(self.chat_avatar),
            'creator': self.creator.username,
            'last_message': self.last_message.text if self.last_message else None
        }


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    last_read_message = models.ForeignKey('message.Message', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'user ' + self.user.username + ' in chat ' + self.chat.title

    def to_json(self):
        return {
            'id': self.id,
            'user_username': self.user.username,
            'chat_id': self.chat.id,
            'last_read_message': self.last_read_message.text if self.last_read_message else None
        }

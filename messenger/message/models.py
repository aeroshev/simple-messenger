from django.db import models
from chats.models import Chat
from users.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/attachment/{1}'.format(instance.user.id, filename)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, default='')
    added_at = models.TimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return 'text ' + self.text

    def to_json(self):
        return {
            'id': self.id,
            'chat_id': self.chat.id,
            'user_id': self.user.id,
            'text': self.text,
            'added_at': str(self.added_at)[:5]
        }


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, null=True, blank=False)
    document = models.FileField(upload_to=user_directory_path, max_length=(10 * 1024 * 1024), null=True, blank=False)
    image = models.ImageField(upload_to=user_directory_path, max_length=(5 * 1024 * 1024), null=True, blank=False)
    audio = models.FileField(upload_to=user_directory_path, max_length=(5 * 1024 * 1024), null=True, blank=False)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return 'type ' + self.type

    def to_json(self):
        file = None
        if self.type == 'image':
            file = self.image
        if self.type == 'document':
            file = self.document
        if self.type == 'audio':
            file = self.audio

        return {
            'message_id': self.message.id,
            'chat_id': self.chat.id,
            'user_id': self.user.id,
            'type': self.type,
            'path': file.url if file is not None else '',
            'name': file.name if file is not None else ''
        }

from django import forms
from .models import Message, Attachment
from chats.models import Member, Chat


class MessageForm(forms.Form):
    chat = forms.ModelChoiceField(queryset=Chat.objects.all(), to_field_name='id', required=True)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_chat(self):
        user = self.user
        chat = self.cleaned_data['chat']

        member = Member.objects.select_related('chat', 'user').filter(chat=chat, user=user)
        if not member:
            self.add_error('user', 'This user are not contain in this chat')
        return chat


class AddMessageForm(MessageForm):
    text = forms.CharField(required=False)
    type = forms.CharField(max_length=8, required=False)
    document = forms.FileField(required=False)
    image = forms.ImageField(required=False)
    audio = forms.FileField(required=False)

    def clean(self):
        attachment_type = self.cleaned_data['type']
        image = self.cleaned_data['image']
        document = self.cleaned_data['document']
        audio = self.cleaned_data['audio']

        if attachment_type:
            if attachment_type == 'image' and image is None:
                self.add_error('type', 'Field image empty')
            if attachment_type == 'document' and document is None:
                self.add_error('type', 'Field document empty')
            if attachment_type == 'audio' and audio is None:
                self.add_error('type', 'Field audio empty')
        return self.cleaned_data

    def save(self):
        data = self.cleaned_data
        user = self.user
        chat = data['chat']
        text = data['text']
        attachment_type = data['type']
        document = data['document']
        image = data['image']
        audio = data['audio']

        if attachment_type == 'image':
            text = 'image'
        if attachment_type == 'document':
            text = 'document'
        if attachment_type == 'audio':
            text = 'audio message'

        message = Message.objects.create(chat=chat, user=user, text=text)
        attachment = Attachment.objects.create(message=message,
                                               chat=chat,
                                               user=user,
                                               type=attachment_type,
                                               document=document,
                                               image=image,
                                               audio=audio)

        tmp = Chat.objects.filter(id=chat.id)
        tmp.update(last_message=message)

        return {'message': message, 'attachment': attachment}


class ReadMessageForm(MessageForm):
    message = forms.ModelChoiceField(queryset=Message.objects.all(), to_field_name='id', required=True)

    def clean_message(self):
        message = self.cleaned_data['message']
        chat = self.cleaned_data['chat']

        if message.chat != chat:
            self.add_error('message', 'This message are not contain in this chat')
        return message

    def save(self):
        data = self.cleaned_data
        message = data['message']
        chat = data['chat']
        reader = self.user

        member = Member.objects.select_related('user', 'chat', 'last_read_message').filter(user=reader, chat=chat)
        member.update(last_read_message=message)

        return member[0]

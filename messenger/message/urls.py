from message.views import add_message, read_message, get_list_messages
from django.urls import path


urlpatterns = [
    path('', get_list_messages, name='get_list_messages'),
    path('new/', add_message, name='add_message'),
    path('read/', read_message, name='read_message')
]

from .views import chat_list, create_chat
from django.urls import path, include


urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('new/', create_chat, name='create_chat')
]

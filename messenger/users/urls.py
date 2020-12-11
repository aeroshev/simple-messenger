from users.views import get_profile, search
from django.urls import path


urlpatterns = [
    path('', get_profile, name='get_profile'),
    path('search/', search, name='search')
]

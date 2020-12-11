from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from auth import views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social_auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('chat/', include('chats.urls')),
    path('user/', include('users.urls')),
    path('message/', include('message.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# noinspection SpellCheckingInspection
"""risto_book_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from risto_book_final import settings
from risto_book_final.views import maintenance, Home, UserCreationView, UserEditView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('maintenance', maintenance, name='maintenance'),
    path('', Home.as_view(), name='home'),
    path('homepage', Home.as_view(), name='home'),
    path('register/', UserCreationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', UserEditView.as_view(), name='profile'),
    path('booking/', include('booking.urls')),
    path('menu/', include('menu.urls')),
    path('manage/', include('admin_tools.urls')),
    path('foto_ricordo/', include('foto_ricordo.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

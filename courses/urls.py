from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import courses

urlpatterns = [
    path('', courses, name='courses'),
]
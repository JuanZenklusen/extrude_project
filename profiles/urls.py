from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import index, RegisterView, CustomLoginView, profile

urlpatterns = [
    path('', index, name='index'),
    path('create_user/', RegisterView.as_view(), name='create_user'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]
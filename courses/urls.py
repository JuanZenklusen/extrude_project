from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import courses, view_course, play_lesson, no_matriculado

urlpatterns = [
    path('', courses, name='courses'),
    path('no_matriculado', no_matriculado, name='no_matriculado'),
    path('<slug:slug>', view_course, name='view_course'),
    path('<slug:slug>/<slug:slug_l>', play_lesson, name='play_lesson'),
]
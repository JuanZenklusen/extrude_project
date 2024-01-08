from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import courses, view_course, play_lesson, no_matriculado, take_exam, comparative_results, submit_homework, send_ticket

urlpatterns = [
    path('', courses, name='courses'),
    path('send_ticket', send_ticket, name='send_ticket'),
    path('submit_homework/<slug:slug>', submit_homework, name='submit_homework'),
    path('no_matriculado', no_matriculado, name='no_matriculado'),
    path('take_exam/<slug:slug>/<int:id>', take_exam, name='take_exam'),
    path('comparative_results/<slug:slug>/<int:id>', comparative_results, name='comparative_results'),
    path('<slug:slug>', view_course, name='view_course'),
    path('<slug:slug>/<slug:slug_l>', play_lesson, name='play_lesson'),
]
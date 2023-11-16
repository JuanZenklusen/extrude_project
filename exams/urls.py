from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import adm_super, add_exam, administrar_examen, add_question, edit_question, delete_question, add_option, edit_option, delete_option, visible_exam

urlpatterns = [
    path('delete_question/<int:id>/<int:id_q>', delete_question, name='delete_question'),
    path('delete_question/<int:id>/<int:id_q>/<int:id_op>', delete_option, name='delete_option'),
    path('adm_exam', adm_super, name='adm_super'),
    path('add_exam/<slug:slug>', add_exam, name='add_exam'),
    path('administrar_examen/<int:id>', administrar_examen, name='administrar_examen'),
    path('administrar_examen/<int:id>/add_question', add_question, name='add_question'),
    path('edit_question/<int:id>/<int:id_q>/', edit_question, name='edit_question'),
    path('administrar_examen/<int:id>/<int:id_q>/add_option', add_option, name='add_option'),
    path('edit_question/<int:id>/<int:id_q>/<int:id_op>/edit_option', edit_option, name='edit_option'),
    path('visible_exam/<int:id>', visible_exam, name='visible_exam')
]
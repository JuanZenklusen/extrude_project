from django.urls import path
from .views import adm_courses, add_course, adm_course, adm_modules_lessons, add_module, edit_module, add_lesson, edit_lesson, add_commission, edit_commission, add_matricula

urlpatterns = [
    path('', adm_courses, name='adm_courses'),
    path('add_course', add_course, name='add_course'),
    path('adm_course/<int:id>', adm_course, name='adm_course'),
    path('adm_modules_lessons/<int:id>', adm_modules_lessons, name='adm_modules_lessons'),
    path('add_module/<int:id>', add_module, name='add_module'),
    path('edit_module/<int:id>', edit_module, name='edit_module'),
    path('add_lesson/<int:id>', add_lesson, name='add_lesson'),
    path('edit_lesson/<int:id>', edit_lesson, name='edit_lesson'),
    path('add_commission/<int:id>', add_commission, name='add_commission'),
    path('edit_commission/<int:id>', edit_commission, name='edit_commission'),
    path('add_matricula/<int:id>', add_matricula, name='add_matricula'),
]
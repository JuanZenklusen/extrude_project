"""
URL configuration for extrude_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import terms_conditions

urlpatterns = [
    path('', include('profiles.urls')),
    path('courses/', include('courses.urls')), #urls.py de courses, hace la logica de la academia de cursos para el usuario
    path('adm_curses/', include('courses.urls_adm')), #urls_adm.py de courses, hace la logica de el administrador de cursos
    path('exams/', include('exams.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('reglamento_de_condiciones_de_acceso_participacion_y_uso_institutodigitaltech', terms_conditions, name='terms_conditions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

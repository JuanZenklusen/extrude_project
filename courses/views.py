from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Courses, Modules, Lessons, Matricula

def no_matriculado(request):
    return render(request, 'no_matriculado.html', {})


def courses(request):
    courses = Courses.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def view_course(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    modules = Modules.objects.filter(course=course).order_by('nro_order')
    return render(request, 'course_slug.html', {'course': course, 'modules': modules})


@login_required
def play_lesson(request, slug, slug_l):
    course = get_object_or_404(Courses, slug=slug)
    lesson = get_object_or_404(Lessons, slug=slug_l)
    
    #matricula = Matricula.objects.filter(user=request.user)
    matricula = Matricula.objects.filter(user=request.user, commission__course=course)

    if not matricula.exists():
        # El usuario no está matriculado en el curso, puedes redirigirlo o mostrar un mensaje de error
        return redirect('no_matriculado')  # Redirige al usuario a la página de inicio, ajusta el nombre de la vista según tu configuración
    
    modules = Modules.objects.filter(course=course).order_by('nro_order')
    return render(request, 'play_lesson.html', {'course': course, 'modules': modules,'lesson': lesson})
    
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import ModuleRating
from .models import Courses, Modules, Lessons, Matricula
from .calc import calcular_porcentaje_avance

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
    matricula = Matricula.objects.filter(user=request.user, commission__course=course)
    advance = calcular_porcentaje_avance(matricula.first(), course)

    if not matricula.exists():
        return redirect('no_matriculado')  # Redirige al usuario a la página de inicio, ajusta el nombre de la vista según tu configuración

    modules = Modules.objects.filter(course=course).order_by('nro_order')

    # Obtén todas las lecciones relacionadas con el curso
    all_lessons = Lessons.objects.filter(module__course=course).order_by('module__nro_order', 'nro_order')
    cantidad_modulos = Modules.objects.filter(course=course).count()

    # Encuentra la lección siguiente en función de la lección actual
    next_lesson = None
    for i, current_lesson in enumerate(all_lessons):
        if current_lesson == lesson and i < len(all_lessons) - 1:
            next_lesson = all_lessons[i + 1]
            break

    # Actualizar el campo 'last_lesson' y 'lessons_viewed' en el objeto Matricula
    if matricula.exists():
        matricula_instance = matricula.first()
        matricula_instance.last_lesson = lesson  # Actualiza la última lección vista
        matricula_instance.lessons_viewed.add(lesson)  # Agrega la lección actual a las lecciones vistas
        matricula_instance.save()

    # Grabar calificación modulo
    if request.method == 'POST':
        # Procesa la calificación del módulo si se envió un formulario POST
        rating = request.POST.get('rating')
        if rating:
            # Verifica si el usuario ya ha calificado este módulo antes
            existing_rating, created = ModuleRating.objects.get_or_create(user=request.user, module=lesson.module)
            existing_rating.rating = rating
            existing_rating.save()

    user_rating = ModuleRating.objects.filter(user=request.user, module=lesson.module).first()

    return render(request, 'play_lesson.html', {'course': course, 
                                                'modules': modules, 
                                                'lesson': lesson, 
                                                'user_rating': user_rating, 
                                                'cantidad_modulos': cantidad_modulos,
                                                'next_lesson': next_lesson,
                                                'advance': advance})

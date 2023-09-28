from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import ModuleRating
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


'''@login_required
def play_lesson(request, slug, slug_l):
    course = get_object_or_404(Courses, slug=slug)
    lesson = get_object_or_404(Lessons, slug=slug_l)
    matricula = Matricula.objects.filter(user=request.user, commission__course=course)

    if not matricula.exists():
        return redirect('no_matriculado')  # Redirige al usuario a la página de inicio, ajusta el nombre de la vista según tu configuración
    
    modules = Modules.objects.filter(course=course).order_by('nro_order')
    cantidad_modulos = modules.count()

    # Grabar calificacion modulo
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
                                                'cantidad_modulos': cantidad_modulos,})'''



'''@login_required
def play_lesson(request, slug, slug_l):
    course = get_object_or_404(Courses, slug=slug)
    lesson = get_object_or_404(Lessons, slug=slug_l)
    matricula = Matricula.objects.filter(user=request.user, commission__course=course)

    if not matricula.exists():
        return redirect('no_matriculado')  # Redirige al usuario a la página de inicio, ajusta el nombre de la vista según tu configuración
    
    modules = Modules.objects.filter(course=course).order_by('nro_order')
    cantidad_modulos = modules.count()

    # Obtén la lección siguiente
    next_lesson = None
    try:
        next_lesson = Lessons.objects.filter(module=lesson.module, nro_order__gt=lesson.nro_order).order_by('nro_order').first()
    except Lessons.DoesNotExist:
        next_lesson = None

    # Grabar calificacion modulo
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
                                                'next_lesson': next_lesson})  # Pasa la lección siguiente al contexto'''



@login_required
def play_lesson(request, slug, slug_l):
    course = get_object_or_404(Courses, slug=slug)
    lesson = get_object_or_404(Lessons, slug=slug_l)
    matricula = Matricula.objects.filter(user=request.user, commission__course=course)

    if not matricula.exists():
        return redirect('no_matriculado')  # Redirige al usuario a la página de inicio, ajusta el nombre de la vista según tu configuración
    
    modules = Modules.objects.filter(course=course).order_by('nro_order')
    cantidad_modulos = modules.count()

    # Obtén la lección siguiente en el mismo módulo
    try:
        next_lesson = Lessons.objects.filter(module=lesson.module, nro_order__gt=lesson.nro_order).order_by('nro_order').first()
    except Lessons.DoesNotExist:
        next_lesson = None

    # Si no hay lección siguiente en el mismo módulo, busca el primer módulo con lecciones en el mismo curso
    if next_lesson is None:
        next_module = Modules.objects.filter(course=course, nro_order__gt=lesson.module.nro_order).order_by('nro_order').first()
        if next_module:
            next_lesson = Lessons.objects.filter(module=next_module).order_by('nro_order').first()

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
                                                'next_lesson': next_lesson})  # Pasa la lección siguiente al contexto


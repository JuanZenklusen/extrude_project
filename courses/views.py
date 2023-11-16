from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.views.generic import ListView
from .models import ModuleRating
from .models import Courses, Modules, Lessons, Matricula, Exam, Question, Option, Commission
from .calc import calcular_porcentaje_avance
from django.urls import reverse
from django.contrib.auth.models import User


def str_price(price):
    return "{:,.2f}".format(price).replace(",", "temp").replace(".", ",").replace("temp", ".")



def no_matriculado(request):
    return render(request, 'no_matriculado.html', {})



def courses(request):
    courses = Courses.objects.filter(visible=True)

    for course in courses:
        if course.price:
            course.formatted_price = str_price(course.price)
        else:
            course.formatted_price = None

        if course.price_payment_installments:
            course.formatted_price_payment_installments = str_price(course.price_payment_installments)
        else:
            course.formatted_price_payment_installments = None

    return render(request, 'courses.html', {'courses': courses})



def view_course(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    modules = Modules.objects.filter(course=course).order_by('nro_order')
    exams = Exam.objects.filter(course = course, visible = True)

    if course.price:
        course.formatted_price = str_price(course.price)
    else:
        course.formatted_price = None

    if course.price_payment_installments:
        course.formatted_price_payment_installments = str_price(course.price_payment_installments)
    else:
        course.formatted_price_payment_installments = None

    if request.user.is_authenticated:
        matricule = Matricula.objects.filter(user=request.user, commission__course=course).first()
        
    else:
        matricule = None

    
    return render(request, 'course_slug.html', {'course': course, 'modules': modules, 'matricule': matricule, 'exams': exams})



@login_required
def play_lesson(request, slug, slug_l):
    course = get_object_or_404(Courses, slug=slug)
    lesson = get_object_or_404(Lessons, slug=slug_l)
    title_lesson = lesson.title
    matricula = Matricula.objects.filter(user=request.user, commission__course=course)
    advance = calcular_porcentaje_avance(matricula.first(), course)
    matricule = matricula

    if not matricula.exists():
        return redirect('no_matriculado')

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
        matricula_instance.last_lesson = lesson
        matricula_instance.lessons_viewed.add(lesson)
        matricula_instance.save()

    # Grabar calificación modulo
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating:
            existing_rating, created = ModuleRating.objects.get_or_create(user=request.user, module=lesson.module)
            existing_rating.rating = rating
            existing_rating.save()

    user_rating = ModuleRating.objects.filter(user=request.user, module=lesson.module).first()
    
    # Manejar el caso en que lesson.pdf es None
    pdf_url = lesson.pdf.url if lesson.pdf else None

    return render(request, 'play_lesson.html', {'course': course, 
                                                'modules': modules, 
                                                'lesson': lesson,
                                                'title_lesson': title_lesson, 
                                                'user_rating': user_rating, 
                                                'cantidad_modulos': cantidad_modulos,
                                                'next_lesson': next_lesson,
                                                'advance': advance,
                                                'pdf_url': pdf_url,
                                                'matricule': matricule})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def adm_courses(request):
    courses = Courses.objects.all

    return render(request, 'adm_courses.html', {'courses': courses,})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_course(request):
    
    if request.method == 'POST':

        name = request.POST.get('course_name')
        description = request.POST.get('course_description')

        if 'course_featured' in request.POST:
            featured = True
        else:
            featured = False
        if 'course_visible' in request.POST:
            visible = True
        else:
            visible = False

        price = float(request.POST.get('course_price').replace(',', '.'))
        price_payment_installments = float(request.POST.get('course_price_payment_installments').replace(',', '.'))
        payment_installments = request.POST.get('course_payment_installments')
        link_mp = request.POST.get('course_link_mp')
        program = request.POST.get('course_program')
        lesson_duration = request.POST.get('course_lesson_duration')
        weekly_frequency = request.POST.get('course_weekly_frequency')
        duration_in_weeks = request.POST.get('course_duration_in_weeks')
        modality = request.POST.get('course_modality')
        requirements = request.POST.get('course_requirements')
        text_include = request.POST.get('course_text_include')

        new_course = Courses.objects.create(
            name=name,
            description=description,
            featured=featured,
            visible=visible,
            price=price,
            price_payment_installments=price_payment_installments,
            payment_installments=payment_installments,
            link_mp=link_mp,
            program=program,
            lesson_duration=lesson_duration,
            weekly_frequency=weekly_frequency,
            duration_in_weeks=duration_in_weeks,
            modality=modality,
            requirements=requirements,
            text_include=text_include
        )

        new_course.save()

        return redirect('adm_courses')

    return render(request, 'partials/adm_course/add_course.html', {})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def adm_course(request, id):
    course = get_object_or_404(Courses, id=id)

    if request.method == 'POST':
        course.name = request.POST.get('course_name')
        course.description = request.POST.get('course_description')

        if 'course_featured' in request.POST:
            course.featured = True
        else:
            course.featured = False
        if 'course_visible' in request.POST:
            course.visible = True
        else:
            course.visible = False
        if 'course_img' in request.FILES:
            course.img = request.FILES.get('course_img')

        # Manejar el caso cuando los valores pueden ser 'None'
        try:
            course.price = float(request.POST.get('course_price').replace(',', '.'))
        except (TypeError, ValueError):
            course.price = None

        try:
            course.price_payment_installments = float(request.POST.get('course_price_payment_installments').replace(',', '.'))
        except (TypeError, ValueError):
            course.price_payment_installments = None

        course.payment_installments = request.POST.get('course_payment_installments')
        course.link_mp = request.POST.get('course_link_mp')
        course.program = request.POST.get('course_program')
        course.lesson_duration = request.POST.get('course_lesson_duration')
        course.weekly_frequency = request.POST.get('course_weekly_frequency')
        course.duration_in_weeks = request.POST.get('course_duration_in_weeks')
        course.modality = request.POST.get('course_modality')
        course.requirements = request.POST.get('course_requirements')
        course.text_include = request.POST.get('course_text_include')
        course.save()

    return render(request, 'partials/adm_course/edit_course.html', {'course': course})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def adm_modules_lessons(request, id):
    course = get_object_or_404(Courses, id=id)

    return render(request, 'partials/adm_course/adm_modules_lessons/adm_modules_lessons.html', {'course': course})


@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_module(request, id):
    course = get_object_or_404(Courses, id = id)
    modules = Modules.objects.filter(course = course)

    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        nro_order = request.POST.get('nro_order')
        course = course
        new_module = Modules.objects.create(title = title, subtitle = subtitle, nro_order = nro_order, course = course)
        return redirect(reverse('adm_modules_lessons', kwargs={'id': id}))
        

    return render(request, 'partials/adm_course/adm_modules_lessons/add_module.html', {'course': course, 'modules': modules})


@user_passes_test(lambda u: u.is_superuser, login_url='index')
def edit_module(request, id):
    module = get_object_or_404(Modules, id = id)
    course = module.course
    modules = Modules.objects.filter(course = course)

    if request.method == 'POST':
        module.title = request.POST.get('title')
        module.subtitle = request.POST.get('subtitle')
        module.nro_order = request.POST.get('nro_order')
        module.save()
        return redirect(reverse('adm_modules_lessons', kwargs={'id': course.id}))

    return render(request, 'partials/adm_course/adm_modules_lessons/edit_module.html', {'module': module, 'course': course, 'modules': modules})


@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_lesson(request, id):
    module = get_object_or_404(Modules, id = id)
    course = module.course

    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle =  request.POST.get('subtitle')
        nro_order =  request.POST.get('nro_order')
        video =  request.POST.get('video')

        pdf = request.FILES.get('pdf')
        
        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')
        text3 = request.POST.get('text3')
        class_materials = request.POST.get('class_materials')
        module_ = module

        
        new_lesson = Lessons.objects.create(
            title = title,
            subtitle = subtitle,
            nro_order = nro_order,
            video = video,
            pdf = pdf,
            text1 = text1,
            text2 = text2,
            text3 = text3,
            class_materials = class_materials,
            module = module_
        )

        return redirect(reverse('adm_modules_lessons', kwargs={'id': course.id}))


    return render(request, 'partials/adm_course/adm_modules_lessons/add_lesson.html', {'module': module, 'course': course})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def edit_lesson(request, id):
    lesson = get_object_or_404(Lessons, id = id)
    module = lesson.module
    course = module.course

    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        nro_order = int(request.POST.get('nro_order'))
        video =  request.POST.get('video')

        pdf_file = request.FILES.get('pdf')
        if pdf_file:
            lesson.pdf = pdf_file

        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')
        text3 = request.POST.get('text3')
        class_materials = request.POST.get('class_materials')

        lesson.title = title
        lesson.subtitle = subtitle
        lesson.nro_order = nro_order
        lesson.video = video
        lesson.text1 = text1
        lesson.text2 = text2
        lesson.text3 = text3
        lesson.class_materials = class_materials
        lesson.save()
        
        return redirect(reverse('adm_modules_lessons', kwargs={'id': course.id}))

    return render(request, 'partials/adm_course/adm_modules_lessons/edit_lesson.html', {'module': module, 'course': course, 'lesson': lesson})


@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_commission(request, id):
    course = get_object_or_404(Courses, id = id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        teacher = request.POST.get('teacher')
        tutor = request.POST.get('tutor')
        base_cert = request.FILES.get('base_cert')

        # Verifica si se cargó un archivo
        if base_cert:
            # Si se cargó un archivo, puedes guardar la imagen
            new_commission = Commission.objects.create(
                name=name,
                date=date,
                teacher=teacher,
                tutor=tutor,
                base_cert=base_cert,
                course = course
            )
        else:
            # Si no se cargó un archivo, utiliza el valor predeterminado
            new_commission = Commission.objects.create(
                name=name,
                date=date,
                teacher=teacher,
                tutor=tutor,
                course = course
            )

        return redirect('adm_courses')

    return render(request, 'partials/commissions/add_commission.html', {'course': course})


@user_passes_test(lambda u: u.is_superuser, login_url='index')
def edit_commission(request, id):
    commission = get_object_or_404(Commission, id = id)
    course = commission.course

    if request.method == 'POST':
        commission.name = request.POST.get('name')
        commission.date = request.POST.get('date')
        commission.teacher = request.POST.get('teacher')
        commission.tutor = request.POST.get('tutor')

        base_cert = request.FILES.get('base_cert')  # Obtener el nuevo archivo si se proporciona

        # Verificar si se proporcionó un nuevo archivo y actualizar el campo base_cert
        if base_cert:
            commission.base_cert = base_cert

        commission.save()

        return redirect('adm_courses')

    return render(request, 'partials/commissions/edit_commission.html', {'course': course, 'commission': commission})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_matricula(request, id):
    commission = get_object_or_404(Commission, id = id)
    users = User.objects.all()

    if request.method == 'POST':
        selected_user_id = request.POST.get('user')
        selected_user = User.objects.get(id=selected_user_id)

        new_matricula = Matricula.objects.create(
            commission = commission,
            user = selected_user
            )
        return redirect('adm_courses')

    return render(request, 'partials/commissions/matricula/add_matricula.html', {'commission': commission, 'users': users})
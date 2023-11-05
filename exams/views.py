from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import user_passes_test
from courses.models import Courses, Modules, Lessons, Matricula, Exam, Question, Option

@user_passes_test(lambda u: u.is_superuser, login_url='index')
def adm_super(request):
    courses = Courses.objects.all()

    return render(request, 'adm_super.html', {'courses': courses,})


@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_exam(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        exam = Exam.objects.create(course=course, name=name, description=description)
        exam.save()

        return redirect('adm_super')


    return render(request, 'add_exam.html', {'course': course,})

@user_passes_test(lambda u: u.is_superuser, login_url='index')
def administrar_examen(request, id):
    exam = get_object_or_404(Exam, id=id)
    questions = Question.objects.filter(exam=exam)

    return render(request, 'administrar_examen.html', 
                  {'exam': exam, 'questions': questions})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_question(request, id):
    exam = get_object_or_404(Exam, id=id)
    questions = Question.objects.filter(exam=exam)

    if request.method == 'POST':
        text = request.POST.get('add_question')
        exam = exam
        new_question = Question.objects.create(exam=exam, text=text)
        new_question.save()
        return redirect(reverse('administrar_examen', kwargs={'id': id}))

    return render(request, 'partials/form_add_question.html', 
                  {'exam': exam, 'questions': questions})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def edit_question(request, id, id_q):
    exam = get_object_or_404(Exam, id=id)
    question = get_object_or_404(Question, id=id_q)
    questions = Question.objects.filter(exam=exam)

    if request.method == 'POST':
        text = request.POST.get('add_question')
        question.text = text
        question.save()
        return redirect(reverse('administrar_examen', kwargs={'id': id}))

    return render(request, 'partials/form_edit_question.html', 
                  {'exam': exam, 'question': question, 
                   'questions': questions})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def delete_question(request, id, id_q):
    exam = get_object_or_404(Exam, id=id)
    question = get_object_or_404(Question, id=id_q)
    questions = Question.objects.filter(exam=exam)

    return redirect(reverse('administrar_examen', kwargs={'id': id}))



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def add_option(request, id, id_q):
    exam = get_object_or_404(Exam, id = id)
    questions = Question.objects.filter(exam=exam)
    question = get_object_or_404(Question, id = id_q)
    
    if request.method == 'POST':
        text = request.POST.get('add_option')
        is_correct = request.POST.get('is_correct') == 'on'
        question_ = question
        
        new_option = Option.objects.create(question = question_, text = text, is_correct = is_correct)
        new_option.save()
        return redirect(reverse('administrar_examen', kwargs={'id': id}))

    return render(request, 'partials/form_add_option.html', 
                  {'exam': exam, 'questions': questions})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def edit_option(request, id, id_q, id_op):
    exam = get_object_or_404(Exam, id=id)
    questions = Question.objects.filter(exam=exam)
    question = get_object_or_404(Question, id=id_q)
    option = get_object_or_404(Option, id=id_op)

    if request.method == 'POST':
        text = request.POST.get('add_option')
        is_correct = request.POST.get('is_correct') == 'on'
        question_ = question
        
        option.text = text
        option.is_correct = is_correct
        option.save()
        return redirect(reverse('administrar_examen', kwargs={'id': id}))

    return render(request, 'partials/form_edit_option.html', 
                  {'exam': exam, 'question': question, 
                   'questions': questions,
                   'option': option})



@user_passes_test(lambda u: u.is_superuser, login_url='index')
def delete_option(request, id, id_q, id_op):
    exam = get_object_or_404(Exam, id=id)
    question = get_object_or_404(Question, id=id_q)
    questions = Question.objects.filter(exam=exam)
    option = get_object_or_404(Option, id=id_op)

    option.delete()

    return redirect(reverse('administrar_examen', kwargs={'id': id}))
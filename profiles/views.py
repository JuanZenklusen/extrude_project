from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404
from courses.models import Courses, Matricula, Modules, Lessons
from courses.calc import calcular_porcentaje_avance
from django.db.models import Count


def index(request):
    featured_courses = Courses.objects.filter(featured=True)
    return render(request, 'index.html', {'featured_courses': featured_courses})


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})
    

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'perfil/password_reset.html'
    email_template_name = 'perfil/password_reset_email.html'
    subject_template_name = 'perfil/password_reset_subject.txt'
    success_message = "Le hemos enviado instrucciones por correo electrónico para restablecer su contraseña," \
                      "si existe una cuenta con el correo electrónico que ingresó debería recibirlos en breve." \
                      " Si no recibe un correo electrónico," \
                      " asegúrese de haber ingresado la dirección con la que se registró y verifique su carpeta de correo no deseado."
    success_url = reverse_lazy('users-home')



@login_required
def profile(request):
    matriculas = Matricula.objects.filter(user=request.user)

    for matricula in matriculas:
        if matricula.last_lesson is None:
            # Si last_lesson es None, asignar la primera lección del primer módulo
            first_module = Modules.objects.filter(course=matricula.commission.course).order_by('nro_order').first()
            if first_module:
                first_lesson = Lessons.objects.filter(module=first_module).order_by('nro_order').first()
                matricula.last_lesson = first_lesson
                matricula.save()

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Su perfil ha sido actualizado')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    # Calcular el porcentaje de avance
    for matricula in matriculas:
        total_lessons = Lessons.objects.filter(module__course=matricula.commission.course).count()
        lessons_viewed = matricula.lessons_viewed.count()
        if total_lessons > 0:
            matricula.advance_percentage = (lessons_viewed / total_lessons) * 100
        else:
            matricula.advance_percentage = 0

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form, 'matriculas': matriculas})
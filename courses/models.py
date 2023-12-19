from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid
from django.dispatch import receiver
import os
from django.utils import timezone


class Courses(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False) #nombre del curso
    description = models.CharField(max_length=300, blank=False, null=False) #descripción del curso
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #precio total
    payment_installments = models.IntegerField(blank=True, null=True, default=1) #cantidad de cuotas
    price_payment_installments = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #precio de la cuota
    link_mp = models.CharField(max_length=100, blank=True, null=True) #link mercadopago
    program = models.CharField(max_length=300, blank=True, null=True) #link programa del cusro
    img = models.ImageField(default='course-default.jpg', upload_to='course_images') #miniatura del curso
    modality = models.CharField(max_length=50, blank=True, null=True,) #clases online o asincrónicas
    requirements = models.TextField(max_length=1500, blank=True, null=True,) #requisitos
    lesson_duration = models.CharField(max_length=20, blank=True, null=True,) #duracion de cada clase en horas
    weekly_frequency = models.CharField(max_length=1, blank=True, null=True,) #cuantas clases por semana
    duration_in_weeks = models.CharField(max_length=50, blank=True, null=True,) #duracion en semanas
    text_include = models.TextField(max_length=1500, blank=True, null=True,) #lo que incluye el curso
    featured = models.BooleanField(default=False) #Aparece o no en destacados?
    visible = models.BooleanField(default=True) #para activar si se ve o no en la tienda
    slug = models.SlugField(null=False, blank=False, unique=True) #slug para el link, se genera automáticamente
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

def set_slug_courses(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        slug = slugify(instance.name)

        while Courses.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.name, str(uuid.uuid4())[:8])
            )

        instance.slug = slug

pre_save.connect(set_slug_courses, sender=Courses)



class Modules(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False) #titulo del módulo
    subtitle = models.CharField(max_length=50, blank=True, null=True) #Subtitulo, no es un campo tan importante
    nro_order = models.IntegerField() #Numero de orden de módulo
    course = models.ForeignKey(Courses, on_delete=models.CASCADE) #Llave foranea al curso que pertenece
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'({self.course.name}) - {self.nro_order}) {self.title} '
    
def set_slug_modules(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Modules.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )

        instance.slug = slug

pre_save.connect(set_slug_modules, sender=Modules)


class Lessons(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    nro_order = models.IntegerField()
    video = models.CharField(max_length=200, blank=True, null=True)
    text1 = models.TextField(null=True, blank=True, default="")
    text2 = models.TextField(null=True, blank=True, default="")
    text3 = models.TextField(null=True, blank=True, default="")
    class_materials = models.CharField(max_length=200, blank=True, null=True)
    pdf = models.FileField(blank=True, null=True, upload_to='pdfs')
    visible = models.BooleanField(default=False)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id} - {self.title}'
    
    def save(self, *args, **kwargs):
        if self.pdf:
            base_name, extension = os.path.splitext(self.pdf.name)
            title = self.title

            unique_name = f"{title}-{timezone.now().strftime('%Y%m%d%H%M%S')}{extension}"
            self.pdf.name = unique_name

        super().save(*args, **kwargs)

def set_slug_lessons(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Lessons.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )

        instance.slug = slug

pre_save.connect(set_slug_lessons, sender=Lessons)


'''
class Lessons(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    nro_order = models.IntegerField()
    video = models.CharField(max_length=200, blank=True, null=True)
    text1 = models.TextField(null=True, blank=True, default="")
    text2 = models.TextField(null=True, blank=True, default="")
    text3 = models.TextField(null=True, blank=True, default="")
    class_materials = models.CharField(max_length=200, blank=True, null=True)
    pdf = models.FileField(blank=True, null=True, upload_to='pdfs')
    visible = models.BooleanField(default=False)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id} - {self.title}'

    def generate_unique_pdf_name(self):
        if self.pdf:
            base_name, extension = os.path.splitext(self.pdf.name)
            random_digits = str(uuid.uuid4())[:8]
            return f"{self.slug}-{random_digits}{extension}"
        return None

@receiver(pre_save, sender=Lessons)
def set_slug_and_rename_pdf(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Lessons.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )

        instance.slug = slug

    # Llamar al método para generar el nuevo nombre del archivo PDF
    new_pdf_name = instance.generate_unique_pdf_name()
    
    # Asignar el nuevo nombre del archivo PDF si es necesario
    if new_pdf_name:
        instance.pdf.name = new_pdf_name'''


class Homework(models.Model): #Crear tarea para una lección/clase específica
    title = models.CharField(max_length=200, blank=False, null=False) #El título de la tarea.
    description = models.TextField(blank=True, null=True) #descripción más detallada de la tarea.
    deadline = models.DateTimeField(blank=True, null=True) #La fecha y hora límite para la entrega de la tarea.
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.title}'


class SubmitHomework(models.Model):
    file = models.FileField(blank=True, null=True, upload_to='homework_files')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.homework.title} - {self.student}'

    def save(self, *args, **kwargs):
        if self.file:
            base_name, extension = os.path.splitext(self.file.name)
            student_username = self.student.username

            # Utilizar solo el nombre del estudiante y la marca de tiempo
            unique_name = f"{student_username}-{timezone.now().strftime('%Y%m%d%H%M%S')}{extension}"
            self.file.name = unique_name

        super().save(*args, **kwargs)


class Commission(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, default="")
    date = models.CharField(max_length=50, blank=False, null=False)
    teacher = models.CharField(max_length=50, blank=True, null=True)
    tutor = models.CharField(max_length=50, blank=True, null=True)
    base_cert = models.ImageField(default='base_cert.png', upload_to='base_cert')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name} - {self.date}'



class Matricula(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_lesson = models.ForeignKey(Lessons, on_delete=models.SET_NULL, blank=True, null=True, related_name='last_lesson_for_matricula')
    lessons_viewed = models.ManyToManyField(Lessons, blank=True, related_name='matriculas_viewed')
    cert_emited = models.BooleanField(default=False, blank=False, null=False)
    name_cert = models.CharField(max_length=100, blank=True, null=True, default="")
    date_cert_emited = models.DateTimeField(null=True, blank=True)
    exam_percentage = models.FloatField(default=0.0, blank=True, null=True) #acumula el ultimo resultado del examen
    approved = models.BooleanField(default=False)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{str(self.id)} - {self.commission.course.name} - {self.user.username}'
    
def set_slug_matricula(sender, instance, *args, **kwargs):
    if instance.user.username and not instance.slug:
        slug = slugify(instance.user.username)

        while Matricula.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.user.username, str(uuid.uuid4())[:8])
            )

        instance.slug = slug

pre_save.connect(set_slug_matricula, sender=Matricula)


class ModuleRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # El usuario que califica el módulo
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)  # El módulo que se está calificando
    rating = models.PositiveSmallIntegerField(default=0, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])  # La calificación de 1 a 5
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'module']  # Un usuario solo puede calificar un módulo una vez

    def __str__(self):
        return str(self.rating)
    

class Exam(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)  # Nombre del examen
    description = models.CharField(max_length=300, blank=False, null=False)  # Descripción del examen
    visible = models.BooleanField(default="False")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.CharField(max_length=400, blank=False, null=False)  # Texto de la pregunta
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=400, blank=False, null=False)  # Texto de la opción
    is_correct = models.BooleanField(default=False)  # Marca si la opción es la correcta
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class StudentExamAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    attempts_remaining = models.IntegerField(default=5)  # Número de intentos permitidos y los que le restan
    last_attempt_timestamp = models.DateTimeField(null=True, blank=True) #Registro de la fecha del ultimo intento

    def can_attempt_exam(self):
        # Verificar si hay intentos restantes y si ha pasado al menos 24 horas desde el último intento
        if self.attempts_remaining > 0:
            if self.last_attempt_timestamp is None or \
                    (timezone.now() - self.last_attempt_timestamp).days >= 1:
                return True
        return False

    def record_attempt(self):
        # Registrar un nuevo intento y actualizar la marca de tiempo del último intento
        if self.can_attempt_exam():
            self.attempts_remaining -= 1
            self.last_attempt_timestamp = timezone.now()
            self.save()

    def __str__(self):
        return f'{self.student.username} - {self.exam.name} - Attempts: {self.attempts_remaining}'


'''class StudentExamAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    attempts_remaining = models.IntegerField(default=5)  # Número de intentos permitidos y los que le restan
    last_attempt_timestamp = models.DateTimeField(null=True, blank=True) #Registro de la fecha del último intento
    selected_options = models.JSONField(null=True, blank=True)  # Almacenar IDs de las respuestas seleccionadas

    def can_attempt_exam(self):
        # Verificar si hay intentos restantes y si ha pasado al menos 24 horas desde el último intento
        if self.attempts_remaining > 0:
            if self.last_attempt_timestamp is None or \
                    (timezone.now() - self.last_attempt_timestamp).days >= 1:
                return True
        return False

    def record_attempt(self, selected_options):
        # Registrar un nuevo intento y actualizar la marca de tiempo del último intento
        if self.can_attempt_exam():
            self.attempts_remaining -= 1
            self.last_attempt_timestamp = timezone.now()
            self.selected_options = selected_options  # Almacenar los IDs de las respuestas seleccionadas
            self.save()

    def __str__(self):
        return f'{self.student.username} - {self.exam.name} - Attempts: {self.attempts_remaining}'''


class QuestionsAndAnswers(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    q1 = models.CharField(max_length=400, default="", null=True) #q representa a las preguntas que le tocaron en el examen, almacena la id de la pregunta
    q2 = models.CharField(max_length=400, default="", null=True)
    q3 = models.CharField(max_length=400, default="", null=True)
    q4 = models.CharField(max_length=400, default="", null=True)
    q5 = models.CharField(max_length=400, default="", null=True)
    q6 = models.CharField(max_length=400, default="", null=True)
    q7 = models.CharField(max_length=400, default="", null=True)
    q8 = models.CharField(max_length=400, default="", null=True)
    q9 = models.CharField(max_length=400, default="", null=True)
    q10 = models.CharField(max_length=400, default="", null=True)
    a1 = models.CharField(max_length=5, default="", null=True) #a representa a las respuestas que marcó como correctas en el ultimo examen, almacena la id de la pregunta
    a2 = models.CharField(max_length=5, default="", null=True)
    a3 = models.CharField(max_length=5, default="", null=True)
    a4 = models.CharField(max_length=5, default="", null=True)
    a5 = models.CharField(max_length=5, default="", null=True)
    a6 = models.CharField(max_length=5, default="", null=True)
    a7 = models.CharField(max_length=5, default="", null=True)
    a8 = models.CharField(max_length=5, default="", null=True)
    a9 = models.CharField(max_length=5, default="", null=True)
    a10 = models.CharField(max_length=5, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.pk}) {self.matricula}-{self.created_at}'

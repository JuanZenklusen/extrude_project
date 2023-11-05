from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid


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
    title = models.CharField(max_length=200, blank=False, null=False) #titulo de la clase
    subtitle = models.CharField(max_length=500, blank=True, null=True) #subtitulo
    nro_order = models.IntegerField() #numero de orden de clase
    video = models.CharField(max_length=200, blank=True, null=True) #Link de video
    document = models.CharField(max_length=200, blank=True, null=True) #Link drive de archivos de la clase
    text1 = models.TextField(null=True, blank=True, default="") #texto 1
    text2 = models.TextField(null=True, blank=True, default="") #texto 2
    text3 = models.TextField(null=True, blank=True, default="") #texto 3
    class_materials = models.CharField(max_length=200, blank=True, null=True) #para agregar un link de drive que contenga powerpoints, excels, entre otros
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id} - {self.title}'


def set_slug_lessons(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Lessons.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )

        instance.slug = slug

pre_save.connect(set_slug_lessons, sender=Lessons)



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
        return self.rating
    

class Exam(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)  # Nombre del examen
    description = models.CharField(max_length=300, blank=False, null=False)  # Descripción del examen
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
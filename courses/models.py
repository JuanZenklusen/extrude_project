from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid


class Courses(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False, default=1000)
    payment_installments = models.IntegerField(blank=True, null=True, default=1) #cantidad de cuotas
    price_payment_installments = models.IntegerField(blank=True, null=True, default=1000)
    link_mp = models.CharField(max_length=100, blank=True, null=True) #link mercadopago
    program = models.CharField(max_length=300, blank=True, null=True)
    img = models.ImageField(default='course-default.jpg', upload_to='course_images')
    modality = models.CharField(max_length=50, blank=True, null=True,) #clases online o asincrónicas
    requirements = models.TextField(max_length=1500, blank=True, null=True,) #requisitos
    lesson_duration = models.CharField(max_length=20, blank=True, null=True,) #duracion de cada clase en horas
    weekly_frequency = models.CharField(max_length=1, blank=True, null=True,) #cuantas clases por semana
    duration_in_weeks = models.CharField(max_length=50, blank=True, null=True,) #duracion en semanas
    course_program = models.CharField(max_length=300, blank=True, null=True,) #link drive del programa del curso
    text_include = models.TextField(max_length=1500, blank=True, null=True,) #lo que incluye el curso
    slug = models.SlugField(null=False, blank=False, unique=True)
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
    title = models.CharField(max_length=100, blank=False, null=False)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    nro_order = models.IntegerField()
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
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
    video = models.CharField(max_length=400, blank=True, null=True)
    text1 = models.TextField(null=True, blank=True, default="")
    text2 = models.TextField(null=True, blank=True, default="")
    text3 = models.TextField(null=True, blank=True, default="")
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


def set_slug_lessons(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Lessons.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )

        instance.slug = slug

pre_save.connect(set_slug_lessons, sender=Lessons)
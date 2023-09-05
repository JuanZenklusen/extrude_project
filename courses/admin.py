from django.contrib import admin
from .models import Courses, Modules, Lessons

class CoursesAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'payment_installments', 'price_payment_installments',
              'link_mp', 'program', 'img', 'modality', 'requirements', 'lesson_duration', 'weekly_frequency',
              'duration_in_weeks', 'course_program', 'text_include')
    list_display = ('id', 'name', 'price', 'slug', 'created_at', 'modified_at')
    search_fields = ('name', 'description', 'price', 'duration_in_weeks')
    list_filter = ('name', 'modality')

admin.site.register(Courses, CoursesAdmin)


class ModulesAdmin(admin.ModelAdmin):
    fields = ('title', 'subtitle', 'nro_order', 'course')
    list_display = ('id', 'title', 'course', 'slug', 'nro_order', 'modified_at')
    search_fields = ('title', 'course')
    list_filter = ('course', 'nro_order')

admin.site.register(Modules, ModulesAdmin)


class LessonsAdmin(admin.ModelAdmin):
    fields = ('title', 'subtitle', 'nro_order', 'video', 'text1',
              'text2', 'text3', 'module')
    list_display = ('id', 'title', 'slug', 'created_at', 'modified_at')
    list_filter = ('module', 'nro_order')

admin.site.register(Lessons, LessonsAdmin)
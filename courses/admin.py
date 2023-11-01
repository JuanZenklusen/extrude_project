from django.contrib import admin
from .models import Courses, Modules, Lessons, Matricula, Commission

class CoursesAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'payment_installments', 'price_payment_installments',
              'link_mp', 'program', 'img', 'modality', 'requirements', 'lesson_duration', 'weekly_frequency',
              'duration_in_weeks', 'text_include', 'featured')
    list_display = ('name', 'id', 'price', 'slug', 'created_at', 'modified_at')
    search_fields = ('name', 'description', 'price', 'duration_in_weeks')
    list_filter = ('name', 'modality')

admin.site.register(Courses, CoursesAdmin)


class ModulesAdmin(admin.ModelAdmin):
    fields = ('title', 'subtitle', 'nro_order', 'course')
    list_display = ('title','id', 'course', 'slug', 'nro_order', 'modified_at')
    search_fields = ('title', 'course')
    list_filter = ('course', 'nro_order')

admin.site.register(Modules, ModulesAdmin)


class LessonsAdmin(admin.ModelAdmin):
    fields = ('title', 'subtitle', 'class_materials', 'nro_order', 'video', 'text1',
              'text2', 'text3', 'module')
    list_display = ('title', 'id', 'slug', 'created_at', 'modified_at')
    list_filter = ('module', 'nro_order')

admin.site.register(Lessons, LessonsAdmin)


class CommissionAdmin(admin.ModelAdmin):
    fields = ('name', 'date', 'teacher', 'tutor', 'base_cert', 'course')
    list_display = ('__str__', 'id')

admin.site.register(Commission, CommissionAdmin)

class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'commission', 'user', 'last_lesson', 'modified_at')
    list_filter = ('commission', 'user', 'created_at', 'modified_at')
    search_fields = ('id', 'user__username', 'commission__course__name')
    filter_horizontal = ('lessons_viewed',)
    readonly_fields = ('last_lesson', 'lessons_viewed', 'slug', 'created_at', 'modified_at') 

    def last_lesson_info(self, obj):
        if obj.last_lesson is None:
            return "Aún no has visto ninguna lección"
        return f"Módulo: {obj.last_lesson.module.nro_order} - Clase: {obj.last_lesson.nro_order} - {obj.last_lesson.title}"
    
    last_lesson_info.short_description = 'Last Lesson'

admin.site.register(Matricula, MatriculaAdmin)

'''
#En caso de que quiera modificar las clases vistas

class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'commission', 'user', 'last_lesson', 'modified_at')
    list_filter = ('commission', 'user', 'created_at', 'modified_at')
    search_fields = ('id', 'user__username', 'commission__course__name')
    filter_horizontal = ('lessons_viewed',)
    readonly_fields = ('last_lesson', 'created_at', 'modified_at')
    
    # Elimina 'id' de fields o fieldsets
    fields = ('commission', 'user', 'last_lesson', 'modified_at', 'lessons_viewed')
    
    def last_lesson_info(self, obj):
        if obj.last_lesson is None:
            return "Aún no has visto ninguna lección"
        return f"Módulo: {obj.last_lesson.module.nro_order} - Clase: {obj.last_lesson.nro_order} - {obj.last_lesson.title}"
    
    last_lesson_info.short_description = 'Last Lesson'

admin.site.register(Matricula, MatriculaAdmin)
'''
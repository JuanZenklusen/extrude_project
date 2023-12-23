from django.contrib import admin
from .models import Courses, Modules, Lessons, Matricula, Commission, Exam, Question, Option, StudentExamAttempt, Homework, SubmitHomework, QuestionsAndAnswers

class CoursesAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'payment_installments', 'price_payment_installments',
              'link_mp', 'program', 'img', 'modality', 'requirements', 'lesson_duration', 'weekly_frequency',
              'duration_in_weeks', 'text_include', 'visible', 'featured')
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
    fields = ('title', 'subtitle', 'nro_order', 'video', 'pdf', 'class_materials', 'text1',
              'text2', 'text3', 'module', 'visible', 'zoom', 'link_zoom', 'day_time')
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
    search_fields = ('id', 'user__username', 'commission__course__name', 'approved')
    filter_horizontal = ('lessons_viewed',)
    readonly_fields = ('exam_percentage', 'approved', 'last_lesson', 'lessons_viewed', 'slug', 'created_at', 'modified_at')

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

class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'description')
    readonly_fields = ('id', 'created_at', 'modified_at')

admin.site.register(Exam, ExamAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'text')
    readonly_fields = ('id', 'created_at', 'modified_at')

admin.site.register(Question, QuestionAdmin)


class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    readonly_fields = ('id', 'created_at', 'modified_at')

admin.site.register(Option, OptionAdmin)


class StudentExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'timestamp', 'attempts_remaining', 'last_attempt_timestamp')
    #readonly_fields = ('student', 'exam', 'timestamp', 'attempts_remaining', 'last_attempt_timestamp')

    def has_add_permission(self, request):
        return False  # No permitir la creación de nuevos objetos StudentExamAttempt desde el panel de administración

admin.site.register(StudentExamAttempt, StudentExamAttemptAdmin)


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'deadline', 'lesson', 'created_at', 'modified_at']
    search_fields = ['title', 'lesson__title', 'lesson__module__course__name']

admin.site.register(Homework, HomeworkAdmin)

class SubmitHomeworkAdmin(admin.ModelAdmin):
    list_display = ['homework', 'student', 'submitted_at']
    search_fields = ['homework__title', 'student__username']

admin.site.register(SubmitHomework, SubmitHomeworkAdmin)


class QuestionsAndAnswersAdmin(admin.ModelAdmin):
    readonly_fields = ('matricula', 'exam', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'created_at')

admin.site.register(QuestionsAndAnswers, QuestionsAndAnswersAdmin)
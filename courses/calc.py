from courses.models import Matricula, Lessons

def calcular_porcentaje_avance(matricula, course):
    # Obtengo el número total de lecciones en el curso actual
    total_lessons_in_course = Lessons.objects.filter(module__course=course).count()

    # Verifico cuántas lecciones ha visto el usuario a través de la relación lessons_viewed
    lessons_vistas = matricula.lessons_viewed.count()

    # Calculo el porcentaje de avance
    porcentaje_avance = (lessons_vistas / total_lessons_in_course) * 100

    return porcentaje_avance


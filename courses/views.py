from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def courses(request):
    return render(request, 'courses.html', {})
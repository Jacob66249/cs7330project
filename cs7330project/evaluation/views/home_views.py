from django.shortcuts import render

from evaluation.models import Course, Department, Faculty, Program


# Create your views here.
def home(request):

    courses = Course.objects.all().count()

    context = {
        "courses": courses,
    }
    return render(request, "evaluation/home.html", context)

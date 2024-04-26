from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from university import models
from .forms import EvaluationForm
from .models import Course, Section, Evaluation

# home
def home(request):
    return render(request, "home.html")


# Course
def list_course(request):
    queryset = models.Course.objects.all().order_by("course_id")
    return render(request, "course/course_list.html", {"queryset": queryset})


def add_course(request):
    if request.method == "GET":
        return render(request, "course/add_course.html")
    course_Id = request.POST.get("course_id")
    name = request.POST.get("name")
    models.Course.objects.create(course_id=course_Id, name=name)
    return redirect("/course/")


def delete_course(request):
    course_Id = request.GET.get("course_id")
    models.Course.objects.filter(course_id=course_Id).delete()
    return redirect("/course/")


def edit_course(request, Course_Id):
    if request.method == "GET":
        row_object = models.Course.objects.filter(course_id=Course_Id).first()
        return render(request, "course/edit_course.html", {"row_object": row_object})

    Name = request.POST.get("name")
    models.Course.objects.filter(course_id=Course_Id).update(name=Name)
    return redirect("/course/")

# evaluation
def enter_evaluation(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    course = section.course
    if request.method == "POST":
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.course = course
            evaluation.section = section
            evaluation.degree_name = course.degree.name
            evaluation.degree_level = course.degree.level
            evaluation.save()
            return redirect('evaluation-list')  # Redirect to an appropriate page
    else:
        form = EvaluationForm()
    return render(request, 'enter_evaluation.html', {
        'form': form,
        'section': section,
        'course': course
    })

def update_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    if request.method == "POST":
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('evaluation-list')  # Redirect to an appropriate page
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'update_evaluation.html', {'form': form, 'evaluation': evaluation})
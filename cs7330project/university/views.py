from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from university import models
from university import models, forms


# home
def home(request):
    return render(request, "home.html")


# Degree
def list_degree(request):
    queryset = models.Degree.objects.all()
    return render(request, "degree/degree_list.html", {"queryset": queryset})


def add_degree(request):
    if request.method == "GET":
        return render(request, "degree/add_degree.html")
    name = request.POST.get("name")
    level = request.POST.get("level")
    models.Degree.objects.create(level=level, name=name)
    return redirect("/degree/")


def edit_degree(request, Name):
    if request.method == "GET":
        row_object = models.Degree.objects.filter(name=Name).first()
        return render(request, "degree/edit_degree.html", {"row_object": row_object})

    Level = request.POST.get("level")
    models.Degree.objects.filter(name=Name).update(level=Level)
    return redirect("/degree/")


def delete_degree(request):
    name = request.GET.get("name")
    level = request.GET.get("level")
    if name and level:
        models.Degree.objects.filter(name=name, level=level).delete()
    return redirect("/degree/")


# DegreeCourse
def list_degreecourse(request):
    queryset = models.DegreeCourse.objects.all()
    return render(
        request, "degreecourse/degreecourse_list.html", {"queryset": queryset}
    )


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


# Instructor
def list_instructor(request):
    queryset = models.Instructor.objects.all()
    return render(request, "instructor/instructor_list.html", {"queryset": queryset})


# Section
def list_section(request):
    queryset = models.Section.objects.all()
    return render(request, "section/section_list.html", {"queryset": queryset})


# Objective
def list_objective(request):
    queryset = models.Objective.objects.all()
    return render(request, "objective/objective_list.html", {"queryset": queryset})


# Evaluation
def list_evaluation(request):
    queryset = models.Evaluation.objects.all()
    return render(request, "evaluation/evaluation_list.html", {"queryset": queryset})

from evaluation.models import Course, Section
from evaluation.forms import (
    AddCourseForm,
    AddSectionForm,
    UpdateCourseForm,
    UpdateSectionForm,
)
from django.shortcuts import redirect, render, get_object_or_404


def course_list(request):
    courses = Course.objects.all().order_by("dept_id", "course_id")
    return render(request, "university/course/course_list.html", {"courses": courses})


def course_detail(request, dept_id, course_id):
    course = get_object_or_404(Course, course_id=course_id, dept_id=dept_id)
    sections = Section.objects.filter(course=course).order_by(
        "semester", "year", "code"
    )
    return render(
        request,
        "university/course/course_detail.html",
        {"course": course, "sections": sections},
    )


def course_create(request):
    if request.method == "POST":
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course-list")
    else:
        form = AddCourseForm()
    return render(request, "university/course/course_create.html", {"form": form})


def course_delete(request, course_id, dept_id):
    courses = get_object_or_404(Course, course_id=course_id, dept_id=dept_id)
    if request.method == "POST":
        courses.delete()
        return redirect("course-list")
    return render(request, "university/course/course_delete.html", {"courses": courses})


def course_update(request, course_id, dept_id):
    course = get_object_or_404(Course, course_id=course_id, dept_id=dept_id)
    if request.method == "POST":
        form = UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course-detail", course.dept_id, course.course_id)
    else:
        form = UpdateCourseForm(instance=course)
    return render(request, "university/course/course_update.html", {"form": form})


def add_section(request, dept_id, course_id):
    if request.method == "POST":
        form = AddSectionForm(dept_id, course_id, request.POST)
        if form.is_valid():
            form.save()
            return redirect("course-detail", dept_id, course_id)
    else:
        form = AddSectionForm(dept_id, course_id)
    return render(
        request,
        "university/course/add_section.html",
        {"form": form, "dept_id": dept_id, "course_id": course_id},
    )


def update_section(request, dept_id, course_id, code, semester, year):
    course = get_object_or_404(Course, course_id=course_id, dept_id=dept_id)
    section = get_object_or_404(
        Section, course=course, code=code, semester=semester, year=year
    )
    if request.method == "POST":
        form = UpdateSectionForm(
            dept_id, course, section, request.POST, instance=section
        )
        if form.is_valid():
            form.save()
            return redirect("course-detail", dept_id, course_id)
    else:
        form = UpdateSectionForm(dept_id, course, section, instance=section)
    return render(
        request,
        "university/course/update_section.html",
        {"form": form, "dept_id": dept_id, "course_id": course_id},
    )


def remove_section(request, dept_id, course_id, code, semester, year):
    course = get_object_or_404(Course, course_id=course_id, dept_id=dept_id)
    section = get_object_or_404(
        Section, course=course, code=code, semester=semester, year=year
    )
    if request.method == "POST":
        section.delete()
        return redirect("course-detail", dept_id, course_id)
    return render(
        request, "university/course/remove_section.html", {"section": section}
    )

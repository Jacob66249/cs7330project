from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from university import models, forms
from django.core.paginator import Paginator


# home
def home(request):
    return render(request, "home.html")


# Degree
def list_degree(request):
    degree_list = models.Degree.objects.all()
    paginator = Paginator(degree_list, 8)  # Display 8 degrees per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "degree/degree_list.html", {"page_obj": page_obj})


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


def degree_details(request):
    form = forms.DegreeQueryForm(request.POST or None)
    context = {"form": form}

    if request.method == "POST" and form.is_valid():
        degree = form.cleaned_data["degree"]

        if degree:
            # Fetch courses associated with the degree
            course_list = models.Course.objects.filter(degreecourse__degree=degree)
            paginator_courses = Paginator(course_list, 5)  # 5 courses per page
            courses_page_number = request.GET.get("courses_page", 1)
            paginated_courses = paginator_courses.get_page(courses_page_number)

            # Fetch sections ordered by year and semester
            section_list = models.Section.objects.filter().order_by("-year", "semester")
            paginator_sections = Paginator(section_list, 5)  # 5 sections per page
            sections_page_number = request.GET.get("sections_page", 1)
            paginated_sections = paginator_sections.get_page(sections_page_number)

            # Fetch all objectives
            objective_list = models.Objective.objects.all()
            paginator_objectives = Paginator(objective_list, 5)  # 5 objectives per page
            objectives_page_number = request.GET.get("objectives_page", 1)
            paginated_objectives = paginator_objectives.get_page(objectives_page_number)

            # Map objectives to courses
            objectives_courses = {}
            for objective in paginated_objectives:
                objectives_courses[objective] = models.Course.objects.filter(
                    objective=objective
                )

            # Update context with paginated data
            context.update(
                {
                    "degree": degree,
                    "courses": paginated_courses,
                    "sections": paginated_sections,
                    "objectives": paginated_objectives,
                    "objectives_courses": objectives_courses,
                }
            )

    return render(request, "degree/degree_details.html", context)


# DegreeCourse
def list_degreecourse(request):
    degreecourse_list = models.DegreeCourse.objects.all()
    paginator = Paginator(degreecourse_list, 8)  # Display 8 degree courses per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "degreecourse/degreecourse_list.html", {"page_obj": page_obj}
    )


# Course
def list_course(request):
    course_list = models.Course.objects.all().order_by("course_id")
    paginator = Paginator(course_list, 8)  # Display 8 courses per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "course/course_list.html", {"page_obj": page_obj})


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


def course_detail(request):
    form = forms.QueryCourseForm(request.POST or None)
    sections = None

    if request.method == "POST" and form.is_valid():
        course = form.cleaned_data["course"]
        year = form.cleaned_data["year"]
        semester = form.cleaned_data["semester"]
        sections = models.Section.objects.filter(
            course=course, year=year, semester=semester
        )
    return render(
        request, "course/course_details.html", {"form": form, "sections": sections}
    )


# Instructor
def list_instructor(request):
    instructor_list = models.Instructor.objects.all()
    paginator = Paginator(instructor_list, 8)  # Display 8 instructors per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "instructor/instructor_list.html", {"page_obj": page_obj})


def instructor_details(request):
    form = forms.QueryInstructorForm(request.POST or None)
    sections = None
    if request.method == "POST" and form.is_valid():
        instructor = form.cleaned_data["instructor"]
        year = form.cleaned_data["year"]
        semester = form.cleaned_data["semester"]
        sections = models.Section.objects.filter(
            instructor=instructor, year=year, semester=semester
        )

    return render(
        request,
        "instructor/instructor_details.html",
        {"form": form, "sections": sections},
    )


# Section
def list_section(request):
    section_list = models.Section.objects.all()
    paginator = Paginator(section_list, 8)  # Display 8 sections per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "section/section_list.html", {"page_obj": page_obj})


# Objective
def list_objective(request):
    objective_list = models.Objective.objects.all()
    paginator = Paginator(objective_list, 8)  # Display 8 objectives per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "objective/objective_list.html", {"page_obj": page_obj})


# Evaluation
def list_evaluation(request):
    evaluation_list = models.Evaluation.objects.all()
    paginator = Paginator(evaluation_list, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "evaluation/evaluation_list.html", {"page_obj": page_obj})

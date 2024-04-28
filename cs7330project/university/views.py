from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from university import models, forms
from .models import Instructor, Section, Degree, Evaluation
from .forms import EvaluationForm, SelectInstructorSectionForm


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
def add_degreecourse(request):
    if request.method == "GET":
        return render(request, "degreecourse/add_degreecourse.html")
    degree = request.POST.get("degree")
    course = request.POST.get("course")
    is_core = request.POST.get("is_core")
    degree_name = request.POST.get("degree_name")
    degree_level = request.POST.get("degree_levl")
    models.DegreeCourse.objects.create(
        degree=degree,
        course=course,
        is_core=is_core,
        degree_name=degree_name,
        degree_level=degree_level,
    )
    return redirect("/degreecourse/")


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
def add_instructor(request):
    if request.method == "GET":
        return render(request, "instructor/add_instructor.html")
    id = request.POST.get("id")
    name = request.POST.get("name")
    models.Instructor.objects.create(name=name, id=id)
    return redirect("/instructor/")


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
def add_section(request):
    if request.method == "GET":
        return render(request, "section/add_section.html")
    Section_Id = request.POST.get("section_id")
    Degree_Id = request.POST.get("degree_id")
    Instructor_Id = request.POST.get("instructor_id")
    Course_Id = request.POST.get("course_id")
    Semester = request.POST.get("semester")
    Year = request.POST.get("year")
    Enrolled_Stu_Num = request.POST.get("enrolled_stu_num")

    models.Section.objects.create(
        degree_id=Degree_Id,
        section_id=Section_Id,
        course_id=Course_Id,
        instructor_id=Instructor_Id,
        semester=Semester,
        year=Year,
        enrolled_stu_num=Enrolled_Stu_Num,
    )
    return redirect("/section/")


def list_section(request):
    section_list = models.Section.objects.all()
    paginator = Paginator(section_list, 8)  # Display 8 sections per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "section/section_list.html", {"page_obj": page_obj})


# Objective
def add_objective(request):
    if request.method == "GET":
        return render(request, "objective/add_objective.html")
    Objective_Code = request.POST.get("objective_code")
    Title = request.POST.get("title")
    Description = request.POST.get("description")
    Course_Id = request.POST.get("course_id")
    models.Objective.objects.create(
        objective_code=Objective_Code,
        title=Title,
        description=Description,
        course_id=Course_Id,
    )
    return redirect("/objective/")


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


def save_evaluation(request, eval_id=None):
    if eval_id:
        evaluation = get_object_or_404(Evaluation, pk=eval_id)
        form = EvaluationForm(request.POST or None, instance=evaluation)
    else:
        form = EvaluationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Evaluation saved successfully!")
            return redirect("/evaluation/")
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, "evaluation/enter_evaluation.html", {"form": form})


def enter_evaluation(request):
    search_performed = False
    evaluations = None
    select_form = SelectInstructorSectionForm(request.POST or None)
    eval_form = EvaluationForm(request.POST or None)

    if request.method == "POST":
        if "search" in request.POST:
            if select_form.is_valid():
                search_performed = True
                instructor = select_form.cleaned_data["instructor"]
                degree = select_form.cleaned_data["degree"]
                semester = select_form.cleaned_data["semester"]

                sections = Section.objects.filter(
                    instructor=instructor, semester=semester, degree=degree
                )

                evaluations = [
                    {
                        "section": section,
                        "evaluation": Evaluation.objects.filter(
                            section=section
                        ).first(),
                        "is_completed": Evaluation.objects.filter(
                            section=section, is_completed=True
                        ).exists(),
                        "improvement_needed": Evaluation.objects.filter(
                            section=section, improvement_needed=True
                        ).exists(),
                    }
                    for section in sections
                ]

        elif "submit_evaluation" in request.POST:
            eval_form = EvaluationForm(request.POST)
            if eval_form.is_valid():
                evaluation = eval_form.save(commit=False)
                section_id = eval_form.cleaned_data["section"]
                evaluation.section = get_object_or_404(Section, pk=section_id)
                evaluation.save()
                return redirect("evaluation-list")
        else:
            eval_form = EvaluationForm()

    context = {
        "select_form": select_form,
        "eval_form": eval_form,
        "evaluations": evaluations,
        "search_performed": search_performed,
    }
    return render(request, "evaluation/enter_evaluation.html", context)


def edit_evaluation(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    evaluation = Evaluation.objects.filter(section=section).first()

    if request.method == "POST":
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect("evaluation-list")  # 重定向到评估列表或其他适当的页面
    else:
        form = EvaluationForm(instance=evaluation)

    context = {"form": form, "section": section}
    return render(request, "evaluation/edit_evaluation.html", context)


# Query involving evaluation

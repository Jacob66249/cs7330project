from .models import (
    Objective,
    Section,
    DegreeCourse,
    Degree
)
from django.db.models import Q


def list_courses_by_degree(degree_id):
    degree_courses = DegreeCourse.objects.filter(degree_id=degree_id).select_related(
        "course"
    )
    course_info = []
    for dc in degree_courses:
        course_info.append(
            {
                "course_id": dc.course.course_id,
                "course_name": dc.course.name,
                "is_core": dc.is_core,
            }
        )
    return course_info


def get_sections_for_degree(degree_id, start_year, end_year, start_semester, end_semester):
    # This function assumes semester importance Spring < Summer < Fall
    semester_order = {'Spring': 1, 'Summer': 2, 'Fall': 3}

    # Fetch the degree object
    degree = Degree.objects.get(id=degree_id)

    # Fetch courses under this degree
    courses = [dc.course for dc in DegreeCourse.objects.filter(degree=degree)]

    # Define a query to find sections within the specified time range
    semester_range_query = (
        Q(year__gt=start_year, year__lt=end_year) | 
        Q(year=start_year, semester__gte=start_semester) | 
        Q(year=end_year, semester__lte=end_semester)
    )

    # Fetch sections that are linked to the courses under this degree within the time range
    sections = Section.objects.filter(
        course__in=courses
    ).filter(semester_range_query).order_by('year', 'semester')

    # Ordering sections by semester importance
    sections = sorted(sections, key=lambda x: (x.year, semester_order[x.semester]))

    return sections


def list_all_objectives():
    objectives = Objective.objects.all()
    return list(objectives.values("objective_code", "title", "description"))


def list_courses_by_objective(*objective_codes):
    objectives = Objective.objects.filter(objective_code__in=objective_codes)
    result = {}
    for obj in objectives:
        courses = obj.courseobjective_set.all().select_related("course")
        result[obj.objective_code] = [
            {"course_id": co.course.course_id, "course_name": co.course.name}
            for co in courses
        ]
    return result

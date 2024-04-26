from django.urls import path
import university.views as views


urlpatterns = [
    path("", views.home, name="home"),
    # Degree
    path("degree/", views.list_degree, name="list_degree"),
    path("degree/add_degree/", views.add_degree, name="add_degree"),
    path("degree/delete_degree/", views.delete_degree, name="delete_degree"),
    path("degree/<str:Name>/edit_degree/", views.edit_degree, name="edit_degree"),
    path("degreecourse/", views.list_degreecourse, name="list_degreecourse"),
    path("degree_details/", views.degree_details, name="degree_detail"),
    # course
    path("course/", views.list_course, name="list_course"),
    path("course/add_course/", views.add_course, name="add_course"),
    path("course/delete_course/", views.delete_course, name="delete_course"),
    path("course/<str:Course_Id>/edit_course/", views.edit_course, name="edit_course"),
    path("course_details/", views.course_detail, name="course_detail"),
    # Instructor
    path("instructor/", views.list_instructor, name="list_instructor"),
    path("instructor_details/", views.instructor_details, name="instructor_detail"),
    # Section
    path("section/", views.list_section, name="list_section"),
    # Objective
    path("objective/", views.list_objective, name="list_objective"),
    # Evaluation
    path("evaluation/", views.list_evaluation, name="list_evaluation"),
]

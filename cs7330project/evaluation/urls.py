from django.urls import path
import evaluation.views as views

urlpatterns = [
    path("", views.home, name="home"),
    # Course
    path("courses/", views.course_list, name="course-list"),
    path("courses/add/", views.course_create, name="course-add"),
    path(
        "courses/<str:dept_id>/<str:course_id>/",
        views.course_detail,
        name="course-detail",
    ),
    path(
        "courses/<str:dept_id>/<str:course_id>/change/",
        views.course_update,
        name="course-update",
    ),
    path(
        "courses/<str:dept_id>/<str:course_id>/remove/",
        views.course_delete,
        name="course-delete",
    ),
]

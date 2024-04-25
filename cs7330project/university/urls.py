from django.urls import path
import university.views as views


urlpatterns = [
    path("", views.home, name="home"),
    # course
    path("course/", views.list_course, name="list_course"),
    path("course/add_course/", views.add_course, name="add_course"),
    path("course/delete_course/", views.delete_course, name="delete_course"),
    path("course/<str:Course_Id>/edit_course/", views.edit_course, name="edit_course"),
]

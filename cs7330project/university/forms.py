from django import forms
from .models import Course, Section, Instructor, Degree


class QueryInstructorForm(forms.Form):
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(), required=True, label="Instructor"
    )
    year = forms.CharField(required=True, label="Year", max_length=4)
    semester = forms.CharField(required=True, label="Semester", max_length=20)

    def __init__(self, *args, **kwargs):
        super(QueryInstructorForm, self).__init__(*args, **kwargs)
        self.fields["instructor"].label_from_instance = lambda obj: obj.name


class QueryCourseForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), required=True, label="Course"
    )
    year = forms.CharField(required=True, label="Year", max_length=4)
    semester = forms.CharField(required=True, label="Semester", max_length=20)

    def __init__(self, *args, **kwargs):
        super(QueryCourseForm, self).__init__(*args, **kwargs)
        self.fields["course"].label_from_instance = lambda obj: obj.name

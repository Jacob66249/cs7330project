from django import forms
from .models import Course, Section, Instructor, Degree

class EvaluationForm(forms.ModelForm):
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=True, label="Section", help_text="Select the section for the evaluation")
    class Meta:
        model = Evaluation
        fields = [
            'section','method', 'levelA_stu_num', 'levelB_stu_num', 
            'levelC_stu_num', 'levelF_stu_num', 'improvement_suggestions'
        ]
        labels = {
            'section': 'Select Section',
            'method': 'Evaluation Method',
            'levelA_stu_num': 'Number of A level students',
            'levelB_stu_num': 'Number of B level students',
            'levelC_stu_num': 'Number of C level students',
            'levelF_stu_num': 'Number of F level students',
            'improvement_suggestions': 'Improvement Suggestions'
        }
from .models import Course, Section, Instructor, Degree


class DegreeQueryForm(forms.Form):
    degree = forms.ModelChoiceField(
        queryset=Degree.objects.all().order_by("name", "level"),
        required=True,
        label="Degree",
    )

    def __init__(self, *args, **kwargs):
        super(DegreeQueryForm, self).__init__(*args, **kwargs)
        self.fields["degree"].label_from_instance = (
            lambda obj: f"{obj.name} ({obj.level})"
        )


class QueryCourseForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), required=True, label="Course"
    )
    year = forms.CharField(required=True, label="Year", max_length=4)
    semester = forms.CharField(required=True, label="Semester", max_length=20)

    def __init__(self, *args, **kwargs):
        super(QueryCourseForm, self).__init__(*args, **kwargs)
        self.fields["course"].label_from_instance = lambda obj: obj.name


class QueryInstructorForm(forms.Form):
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(), required=True, label="Instructor"
    )
    year = forms.CharField(required=True, label="Year", max_length=4)
    semester = forms.CharField(required=True, label="Semester", max_length=20)

    def __init__(self, *args, **kwargs):
        super(QueryInstructorForm, self).__init__(*args, **kwargs)
        self.fields["instructor"].label_from_instance = lambda obj: obj.name

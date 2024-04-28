from django import forms
from .models import Course, Section, Instructor, Degree,Evaluation

class EvaluationForm(forms.ModelForm):
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=True, label="Section", help_text="Select the section for the evaluation")

    class Meta:
        model = Evaluation
        fields = ['section','method', 'levelA_stu_num', 'levelB_stu_num', 'levelC_stu_num', 'levelF_stu_num', 'improvement_suggestions']
        widgets = {
            'method': forms.TextInput(attrs={'class': 'form-control'}),
            'levelA_stu_num': forms.NumberInput(attrs={'class': 'form-control'}),
            'levelB_stu_num': forms.NumberInput(attrs={'class': 'form-control'}),
            'levelC_stu_num': forms.NumberInput(attrs={'class': 'form-control'}),
            'levelF_stu_num': forms.NumberInput(attrs={'class': 'form-control'}),
            'improvement_suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SelectInstructorSectionForm(forms.Form):
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(),
        label="Instructor",
        help_text="Select an instructor",
        required=True
    )
    degree = forms.ModelChoiceField(
        queryset=Degree.objects.all(),
        label="Degree",
        help_text="Select a degree",
        required=True
    )
    semester = forms.ChoiceField(
        choices=Section.SEMESTER_CHOICES,
        label="Semester",
        help_text="Select the semester",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(SelectInstructorSectionForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].label_from_instance = lambda obj: obj.name
        self.fields['degree'].label_from_instance = lambda obj: f"{obj.name} ({obj.level})"

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

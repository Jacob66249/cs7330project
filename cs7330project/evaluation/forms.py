from django import forms
from .models import (
    Degree,
    Course,
    LearningObjective,
    ObjectiveEvaluation,
    Section,
    Instructor,
)


class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ["name", "level", "core_courses"]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_number", "name", "degrees", "objectives"]


class LearningObjectiveForm(forms.ModelForm):
    class Meta:
        model = LearningObjective
        fields = ["code", "title", "description"]


class ObjectiveEvaluationForm(forms.ModelForm):
    class Meta:
        model = ObjectiveEvaluation
        fields = [
            "section",
            "objective",
            "evaluation_method",
            "num_students_A",
            "num_students_B",
            "num_students_C",
            "num_students_F",
            "improvement_suggestions",
        ]


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = [
            "semester_offered",
            "section_number",
            "students_enrolled",
            "instructor",
        ]


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ["id", "name"]

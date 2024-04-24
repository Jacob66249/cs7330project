from django.db import models


class Degree(models.Model):
    name = models.CharField(max_length=100)
    LEVEL_CHOICES = [
        ("BS", "Bachelor of Science"),
        ("MS", "Master of Science"),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    core_courses = models.ManyToManyField(
        "Course", related_name="degree_core_for", blank=True
    )

    class Meta:
        unique_together = ("name", "level")

    def __str__(self):
        return f"{self.name} ({self.level})"


class Course(models.Model):
    course_number = models.CharField(max_length=8, unique=True)  # E.g., CS1010
    name = models.CharField(max_length=255, unique=True)
    degrees = models.ManyToManyField(Degree, related_name="courses")

    def __str__(self):
        return f"{self.course_number} - {self.name}"


class SemesterOffered(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester_name = models.CharField(max_length=10)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.course.name} - {self.semester_name} {self.year}"


class Section(models.Model):
    semester_offered = models.ForeignKey(
        SemesterOffered, on_delete=models.CASCADE, related_name="sections"
    )
    section_number = models.CharField(max_length=3)
    students_enrolled = models.IntegerField(default=0)
    instructor = models.ForeignKey("Instructor", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Section {self.section_number} of {self.semester_offered.course.name}"


class Instructor(models.Model):
    id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LearningObjective(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.title}"


class Course(models.Model):
    # Existing fields from previous model definition...
    objectives = models.ManyToManyField(LearningObjective, related_name="courses")


class EvaluationMethod(models.TextChoices):
    HOMEWORK = "Homework", "Homework"
    PROJECT = "Project", "Project"
    QUIZ = "Quiz", "Quiz"
    ORAL_PRESENTATION = "Oral Presentation", "Oral Presentation"
    REPORT = "Report", "Report"
    MID_TERM = "Mid-term", "Mid-term"
    FINAL_EXAM = "Final Exam", "Final Exam"


class ObjectiveEvaluation(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="objective_evaluations"
    )
    objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    evaluation_method = models.CharField(
        max_length=20, choices=EvaluationMethod.choices
    )
    num_students_A = models.PositiveIntegerField(default=0)
    num_students_B = models.PositiveIntegerField(default=0)
    num_students_C = models.PositiveIntegerField(default=0)
    num_students_F = models.PositiveIntegerField(default=0)
    improvement_suggestions = models.TextField(blank=True)

    def __str__(self):
        return f"Evaluation for {self.objective.title} in {self.section.semester_offered.course.name}"

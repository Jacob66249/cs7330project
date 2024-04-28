from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Degree(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=50)

    class Meta:
        unique_together = ("name", "level")


class Course(models.Model):
    course_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255, unique=True)


class DegreeCourse(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_core = models.BooleanField(default=False)
    degree_name = models.CharField(max_length=255, default="Default Name")
    degree_level = models.CharField(max_length=50, default="Default Level")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.degree_name = self.degree.name
            self.degree_level = self.degree.level
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("degree", "course")


class Instructor(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)


class Section(models.Model):
    SEMESTER_CHOICES = [
        ("Spring", "Spring"),
        ("Summer", "Summer"),
        ("Fall", "Fall"),
    ]

    degree = models.ForeignKey(
        Degree, on_delete=models.CASCADE, related_name="sections"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="sections"
    )
    section_id = models.CharField(
        max_length=3, validators=[MaxValueValidator(999), MinValueValidator(100)]
    )
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    enrolled_stu_num = models.IntegerField()

    class Meta:
        unique_together = ("course", "section_id", "semester", "year", "degree")


class Objective(models.Model):
    objective_code = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Evaluation(models.Model):
    evaluate_id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=255)
    levelA_stu_num = models.IntegerField(null=True, blank=True)
    levelB_stu_num = models.IntegerField(null=True, blank=True)
    levelC_stu_num = models.IntegerField(null=True, blank=True)
    levelF_stu_num = models.IntegerField(null=True, blank=True)
    improvement_suggestions = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=255, default="Default Name")
    degree_level = models.CharField(max_length=50, default="Default Level")
    is_completed = models.BooleanField(default=False)
    improvement_needed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.section:
            self.degree_name = self.section.degree.name
            self.degree_level = self.section.degree.level
        else:
            raise ValueError("Section must be set before saving Evaluation.")
        super().save(*args, **kwargs)


class EvaluatorObjective(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("evaluation", "objective")

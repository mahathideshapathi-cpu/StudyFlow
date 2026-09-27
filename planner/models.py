from django.db import models
from django.contrib.auth.models import User


# =========================================================
# PROFILE
# =========================================================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    daily_study_goal = models.PositiveIntegerField(
        default=2
    )

    preferred_study_time = models.CharField(
        max_length=50,
        default="Evening"
    )

    def __str__(self):

        return self.user.username


# =========================================================
# SUBJECT
# =========================================================

class Subject(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=30,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    exam_date = models.DateField(
        null=True,
        blank=True
    )

    target_grade = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================================================
# TOPIC
# =========================================================

class Topic(models.Model):

    DIFFICULTY_CHOICES = [

        ("Easy", "Easy"),

        ("Medium", "Medium"),

        ("Hard", "Hard"),

    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="topics"
    )

    name = models.CharField(
        max_length=200
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="Medium"
    )

    completion = models.PositiveIntegerField(
        default=0
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):

        return self.name


# =========================================================
# TASK
# =========================================================

class Task(models.Model):

    PRIORITY_CHOICES = [

        ("Low", "Low"),

        ("Medium", "Medium"),

        ("High", "High"),

    ]

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("In Progress", "In Progress"),

        ("Completed", "Completed"),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    date = models.DateField()

    start_time = models.TimeField(
        null=True,
        blank=True
    )

    duration = models.PositiveIntegerField(
        default=60
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title


# =========================================================
# STUDY SESSION
# =========================================================

class StudySession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_sessions"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField()

    start_time = models.TimeField()

    duration = models.PositiveIntegerField(
        default=25
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.subject} - {self.date}"


# =========================================================
# AI STUDY PLAN
# =========================================================

class StudyPlan(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_plans"
    )

    title = models.CharField(
        max_length=200,
        default="My Study Plan"
    )

    plan_data = models.JSONField(
        default=dict
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title
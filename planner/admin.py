from django.contrib import admin
from .models import Profile, Subject, Topic, Task, StudySession, StudyPlan


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "daily_study_goal",
        "preferred_study_time",
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "user",
        "exam_date",
        "target_grade",
    )
    search_fields = ("name", "code")
    list_filter = ("exam_date",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subject",
        "difficulty",
        "completion",
        "deadline",
    )
    list_filter = ("difficulty",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "subject",
        "date",
        "priority",
        "status",
        "duration",
    )
    list_filter = ("priority", "status", "date")
    search_fields = ("title",)


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subject",
        "topic",
        "date",
        "start_time",
        "duration",
        "completed",
    )
    list_filter = ("completed", "date")


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "created_at",
        "updated_at",
    )
    search_fields = ("title",)

from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.landing, name="landing"),

    # Authentication
    path("signup/", views.signup, name="signup"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Settings
    path("settings/", views.settings_page, name="settings"),

    # Subjects & Topics
    path("subjects/", views.subjects, name="subjects"),
    path(
        "subjects/<int:subject_id>/topics/",
        views.topics,
        name="topics"
    ),

    # Tasks
    path("tasks/", views.tasks, name="tasks"),
    path(
        "tasks/<int:task_id>/complete/",
        views.complete_task,
        name="complete_task"
    ),

    # AI Planner
    path("ai-planner/", views.ai_planner, name="ai_planner"),

    # Saved AI Plans
    path("saved-plans/", views.saved_plans, name="saved_plans"),
    path(
        "saved-plans/<int:plan_id>/",
        views.view_plan,
        name="view_plan"
    ),
    path(
        "saved-plans/<int:plan_id>/delete/",
        views.delete_plan,
        name="delete_plan"
    ),
]
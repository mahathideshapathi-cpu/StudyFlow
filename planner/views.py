from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import os
import json

from dotenv import load_dotenv
from google import genai

from .forms import SignupForm
from .models import (
    Subject,
    Topic,
    Task,
    StudySession,
    StudyPlan,
)


# =========================================================
# GEMINI SETUP
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_client = None

if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(
            GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        )
    except Exception as e:
        print(
            "Gemini client setup error:",
            repr(e)
        )
        gemini_client = None


# =========================================================
# LANDING PAGE
# =========================================================

def landing(request):

    return render(
        request,
        "planner/landing.html"
    )


# =========================================================
# SIGNUP
# =========================================================

def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect("dashboard")

    else:

        form = SignupForm()

    return render(
        request,
        "planner/signup.html",
        {
            "form": form
        }
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    user = request.user

    subjects = Subject.objects.filter(
        user=user
    )

    today = timezone.localdate()

    today_tasks = Task.objects.filter(
        user=user,
        date=today
    ).order_by("start_time")

    completed_tasks = Task.objects.filter(
        user=user,
        status="Completed"
    ).count()

    total_tasks = Task.objects.filter(
        user=user
    ).count()

    study_sessions = StudySession.objects.filter(
        user=user
    )

    total_study_minutes = sum(
        session.duration
        for session in study_sessions
    )

    if total_tasks > 0:

        progress = int(
            (completed_tasks / total_tasks) * 100
        )

    else:

        progress = 0

    return render(
        request,
        "planner/dashboard.html",
        {
            "subjects": subjects,
            "today_tasks": today_tasks,
            "completed_tasks": completed_tasks,
            "total_study_minutes": total_study_minutes,
            "progress": progress,
        }
    )


# =========================================================
# SETTINGS
# =========================================================

@login_required
def settings_page(request):

    return render(
        request,
        "planner/settings.html"
    )


# =========================================================
# SUBJECTS
# =========================================================

@login_required
def subjects(request):

    user = request.user

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        code = request.POST.get(
            "code",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        exam_date = request.POST.get(
            "exam_date"
        )

        target_grade = request.POST.get(
            "target_grade",
            ""
        ).strip()

        if name:

            Subject.objects.create(
                user=user,
                name=name,
                code=code,
                description=description,
                exam_date=(
                    exam_date
                    if exam_date
                    else None
                ),
                target_grade=target_grade,
            )

        return redirect("subjects")

    user_subjects = Subject.objects.filter(
        user=user
    ).order_by("name")

    return render(
        request,
        "planner/subjects.html",
        {
            "subjects": user_subjects
        }
    )


# =========================================================
# TOPICS
# =========================================================

@login_required
def topics(request, subject_id):

    user = request.user

    try:

        subject = Subject.objects.get(
            id=subject_id,
            user=user
        )

    except Subject.DoesNotExist:

        return redirect("subjects")

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        difficulty = request.POST.get(
            "difficulty",
            "Medium"
        )

        deadline = request.POST.get(
            "deadline"
        )

        if name:

            Topic.objects.create(
                subject=subject,
                name=name,
                difficulty=difficulty,
                deadline=(
                    deadline
                    if deadline
                    else None
                ),
            )

        return redirect(
            "topics",
            subject_id=subject.id
        )

    subject_topics = Topic.objects.filter(
        subject=subject
    ).order_by("name")

    return render(
        request,
        "planner/topics.html",
        {
            "subject": subject,
            "topics": subject_topics
        }
    )


# =========================================================
# TASKS
# =========================================================

@login_required
def tasks(request):

    user = request.user

    user_subjects = Subject.objects.filter(
        user=user
    ).order_by("name")

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        subject_id = request.POST.get(
            "subject"
        )

        description = request.POST.get(
            "description",
            ""
        ).strip()

        date = request.POST.get(
            "date"
        )

        start_time = request.POST.get(
            "start_time"
        )

        duration = request.POST.get(
            "duration",
            60
        )

        priority = request.POST.get(
            "priority",
            "Medium"
        )

        subject = None

        if subject_id:

            try:

                subject = Subject.objects.get(
                    id=subject_id,
                    user=user
                )

            except Subject.DoesNotExist:

                subject = None

        if title and date:

            Task.objects.create(
                user=user,
                subject=subject,
                title=title,
                description=description,
                date=date,
                start_time=(
                    start_time
                    if start_time
                    else None
                ),
                duration=int(duration),
                priority=priority,
            )

        return redirect("tasks")

    user_tasks = Task.objects.filter(
        user=user
    ).select_related(
        "subject",
        "topic"
    ).order_by(
        "date",
        "start_time"
    )

    return render(
        request,
        "planner/tasks.html",
        {
            "subjects": user_subjects,
            "tasks": user_tasks
        }
    )


# =========================================================
# COMPLETE TASK
# =========================================================

@login_required
def complete_task(request, task_id):

    try:

        task = Task.objects.get(
            id=task_id,
            user=request.user
        )

    except Task.DoesNotExist:

        return redirect("tasks")

    task.status = "Completed"

    task.save()

    return redirect("tasks")


# =========================================================
# AI STUDY PLANNER
# =========================================================

@login_required
def ai_planner(request):

    user = request.user

    user_subjects = Subject.objects.filter(
        user=user
    ).order_by("name")

    plan = None
    error = None

    if request.method == "POST":

        subject_id = request.POST.get(
            "subject"
        )

        topics_text = request.POST.get(
            "topics",
            ""
        ).strip()

        exam_date = request.POST.get(
            "exam_date",
            ""
        )

        study_hours = request.POST.get(
            "study_hours",
            "2"
        )

        difficulty = request.POST.get(
            "difficulty",
            "Medium"
        )

        preferred_time = request.POST.get(
            "preferred_time",
            "Evening"
        )

        # -------------------------------------------------
        # FIND SUBJECT
        # -------------------------------------------------

        try:

            subject = Subject.objects.get(
                id=subject_id,
                user=user
            )

        except (
            Subject.DoesNotExist,
            TypeError,
            ValueError
        ):

            subject = None

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not subject:

            error = (
                "Please select a valid subject."
            )

        elif not topics_text:

            error = (
                "Please enter the topics "
                "you want to study."
            )

        elif not exam_date:

            error = (
                "Please select your exam date."
            )

        else:

            # -------------------------------------------------
            # AI PROMPT
            # -------------------------------------------------

            prompt = f"""
You are StudyFlow AI, an intelligent college study planner.

Create a realistic personalized study plan.

Subject:
{subject.name}

Topics:
{topics_text}

Exam Date:
{exam_date}

Available Study Hours Per Day:
{study_hours}

Difficulty:
{difficulty}

Preferred Study Time:
{preferred_time}

Return ONLY valid JSON.

Do not include markdown.
Do not include ```json.
Do not include explanations outside JSON.

Use exactly this structure:

{{
    "subject": "{subject.name}",
    "exam_date": "{exam_date}",
    "study_hours": "{study_hours}",
    "difficulty": "{difficulty}",
    "days": [
        {{
            "day": 1,
            "title": "Day 1",
            "focus": "Topic name",
            "duration": "60 minutes",
            "tasks": [
                "Learn the basic concepts",
                "Read class notes",
                "Practice questions",
                "Make short revision notes"
            ]
        }}
    ],
    "final_revision": [
        "Revise important concepts",
        "Practice previous questions",
        "Review weak topics"
    ],
    "motivation": "Short encouraging message"
}}

Important rules:

1. Divide the provided topics across multiple days.
2. Do not overload one day.
3. Include concept learning.
4. Include practice questions.
5. Include revision.
6. Keep tasks realistic for a college student.
7. Use the available study hours.
8. Create as many days as reasonably required.
9. The final revision section must contain useful revision activities.
10. Return ONLY valid JSON.
"""

            # -------------------------------------------------
            # GEMINI AI
            # -------------------------------------------------

            if gemini_client:

                try:

                    print(
                        "Sending request to Gemini..."
                    )

                    response = (
                        gemini_client
                        .models
                        .generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )
                    )

                    response_text = (
                        response.text.strip()
                    )

                    # Remove markdown code fences
                    if response_text.startswith(
                        "```json"
                    ):

                        response_text = (
                            response_text[7:]
                            .replace("```", "")
                            .strip()
                        )

                    elif response_text.startswith(
                        "```"
                    ):

                        response_text = (
                            response_text[3:]
                            .replace("```", "")
                            .strip()
                        )

                    # Convert JSON into Python dictionary
                    plan = json.loads(
                        response_text
                    )

                    print(
                        "Gemini AI plan generated successfully."
                    )

                except Exception as e:

                    print(
                        "Gemini API Error:",
                        repr(e)
                    )

                    error = (
                        f"Gemini API Error: {str(e)}"
                    )

                    plan = None

            else:

                error = (
                    "Gemini client could not be initialized. "
                    "Check your GEMINI_API_KEY in .env."
                )

            # -------------------------------------------------
            # BACKUP PLANNER
            # -------------------------------------------------

            if not plan:

                print(
                    "Using StudyFlow backup planner..."
                )

                topics_list = [
                    topic.strip()
                    for topic in topics_text.split(",")
                    if topic.strip()
                ]

                days = []

                for index, topic in enumerate(
                    topics_list[:7],
                    start=1
                ):

                    days.append(
                        {
                            "day": index,
                            "title": f"Day {index}",
                            "focus": topic,
                            "duration": (
                                f"{study_hours} hours"
                            ),
                            "tasks": [
                                "Understand the basic concepts",
                                "Read your class notes",
                                "Practice questions",
                                "Make short revision notes",
                            ],
                        }
                    )

                if not days:

                    days.append(
                        {
                            "day": 1,
                            "title": "Day 1",
                            "focus": "Important concepts",
                            "duration": (
                                f"{study_hours} hours"
                            ),
                            "tasks": [
                                "Read the important concepts",
                                "Study your class notes",
                                "Practice questions",
                                "Make revision notes",
                            ],
                        }
                    )

                plan = {
                    "subject": subject.name,
                    "exam_date": exam_date,
                    "study_hours": study_hours,
                    "difficulty": difficulty,
                    "days": days,
                    "final_revision": [
                        "Revise important concepts",
                        "Practice previous questions",
                        "Review weak topics",
                        "Take a self-test",
                        "Review important formulas",
                    ],
                    "motivation": (
                        "Small progress every day "
                        "leads to big results! 🚀"
                    ),
                }

            # -------------------------------------------------
            # SAVE STUDY PLAN
            # -------------------------------------------------

            try:

                StudyPlan.objects.create(
                    user=user,
                    title=(
                        f"{subject.name} Study Plan"
                    ),
                    plan_data=plan
                )

                print(
                    "Study plan saved successfully."
                )

            except Exception as e:

                print(
                    "Study plan save error:",
                    repr(e)
                )

    # -----------------------------------------------------
    # DISPLAY AI PLANNER
    # -----------------------------------------------------

    return render(
        request,
        "planner/ai_planner.html",
        {
            "subjects": user_subjects,
            "plan": plan,
            "error": error,
        }
    )


# =========================================================
# SAVED STUDY PLANS
# =========================================================

@login_required
def saved_plans(request):

    plans = StudyPlan.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "planner/saved_plans.html",
        {
            "plans": plans
        }
    )


# =========================================================
# VIEW SAVED PLAN
# =========================================================

@login_required
def view_plan(request, plan_id):

    try:

        plan = StudyPlan.objects.get(
            id=plan_id,
            user=request.user
        )

    except StudyPlan.DoesNotExist:

        return redirect("saved_plans")

    return render(
        request,
        "planner/view_plan.html",
        {
            "plan": plan
        }
    )


# =========================================================
# DELETE SAVED PLAN
# =========================================================

@login_required
def delete_plan(request, plan_id):

    if request.method == "POST":

        try:

            plan = StudyPlan.objects.get(
                id=plan_id,
                user=request.user
            )

            plan.delete()

        except StudyPlan.DoesNotExist:

            pass

    return redirect("saved_plans")
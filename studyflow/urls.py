from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Planner app URLs
    path("", include("planner.urls")),

    # Login
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="planner/login.html"
        ),
        name="login",
    ),

    # Logout
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    # Inloggen / uitloggen
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Gebruikersbeheer
    path("list/", views.UserListView.as_view(), name="user-list"),
    path("add/", views.UserCreateView.as_view(), name="user-add"),
    path("<int:pk>/edit/", views.UserUpdateView.as_view(), name="user-edit"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),

    # Groepenbeheer
    path("groups/", views.GroupListView.as_view(), name="group-list"),
    path("groups/add/", views.GroupCreateView.as_view(), name="group-add"),
    path("groups/<int:pk>/edit/", views.GroupUpdateView.as_view(), name="group-edit"),
    path("groups/<int:pk>/delete/", views.GroupDeleteView.as_view(), name="group-delete"),
]

urlpatterns += [
        path("password_change/", views.CustomPasswordChangeView.as_view(), name="password-change"),
        path("password_change/done/", views.CustomPasswordChangeDoneView.as_view(), name="password-change-done"),
]
# Password reset (via e-mail)
urlpatterns += [
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]

# Preferences
urlpatterns += [
    path("preferences/", views.preferences, name="preferences"),
]



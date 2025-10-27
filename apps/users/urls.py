from django.urls import path
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


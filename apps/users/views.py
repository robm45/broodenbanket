from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .forms import CustomUserUpdateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import views as auth_views

# --- Gebruikersbeheer ---
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "users/user_form_create.html"
    success_url = reverse_lazy("users:user-list")

class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = "users/user_form_update.html"
    success_url = reverse_lazy("users:user-list")


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:user-list")
    template_name = "users/user_confirm_delete.html"
    permission_required = "auth.delete_user"

# --- Groepenbeheer ---
class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "users/group_list.html"

class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Group
    fields = ["name", "permissions"]
    success_url = reverse_lazy("users:group-list")
    template_name = "users/group_form.html"
    permission_required = "auth.add_group"

class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Group
    fields = ["name", "permissions"]
    success_url = reverse_lazy("users:group-list")
    template_name = "users/group_form.html"
    permission_required = "auth.change_group"

class GroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy("users:group-list")
    template_name = "users/group_confirm_delete.html"
    permission_required = "auth.delete_group"

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:password-change-done")

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "users/password_change_done.html"

def logout_view(request):
    logout(request)
    return redirect('welkom')

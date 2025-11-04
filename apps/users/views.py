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
from django.contrib.auth.decorators import login_required
from.models import UserProfile
from django.contrib import messages

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

    def form_valid(self, form):
        response = super().form_valid(form)

        # 🔒 Belangrijk: als je iemand anders bewerkt, niet inloggen als die persoon
        if self.request.user.pk != self.object.pk:
            # Forceer dat de sessie ingelogd blijft als de oorspronkelijke gebruiker
            # (Django doet dit soms automatisch verkeerd bij User.save())
            self.request.user.refresh_from_db()

        return response



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

@login_required
def preferences(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        wants_mail = "receive_monthly_mail" in request.POST
        profile.receive_monthly_mail = "receive_monthly_mail" in request.POST
        profile.save()

        if wants_mail:
            messages.success(request, "Je bent ingeschreven voor maandelijks receptenrapport.")
        else:

            messages.info(request, "Je bent uitgeschreven voor maandelijks receptenrapport.")
        return redirect("welkom")

    return render(request, "users/preferences.html", {"profile": profile})


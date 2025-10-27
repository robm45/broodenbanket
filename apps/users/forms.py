from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    is_active = forms.BooleanField(initial=True, required=False)
    is_staff = forms.BooleanField(initial=False, required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "is_active", "is_staff", "groups", "password1", "password2"]


class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    is_active = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ["username", "email", "is_active", "is_staff", "groups"]


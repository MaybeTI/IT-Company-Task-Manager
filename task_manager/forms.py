from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from task_manager.models import Task, Position
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm,
)


class TaskForm(forms.ModelForm):
    CHOICES = (
        (None, "Select a priority"),
        ("Low", "Low"),
        ("Middle", "Middle"),
        ("High", "High"),
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Description",
                "class": "form-control auto-resize",
                "style": "height: 100px; position: relative;",
            }
        )
    )
    deadline = forms.CharField(
        widget=forms.TextInput(attrs={"type": "date", "class": "form-control"})
    )

    is_completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "style": "width: 20px; height: 20px;",
            }
        ),
    )

    priority = forms.CharField(widget=forms.Select(choices=CHOICES))

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"style": "width: 20px; height: 20px;"}
        ),
    )

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        deadline_date = date.fromisoformat(deadline)
        if deadline_date <= date.today():
            raise forms.ValidationError("Deadline should be a future date")
        return deadline


class TaskUpdateWorkersForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"style": "width: 20px; height: 20px; overflow-y: scroll;"}
        ),
    )

    class Meta:
        model = Task
        fields = ("assignees",)


class WorkerCreateForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2", "position")


class WorkerUpdateForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "position",
        )


class WorkerUpdateDescriptionForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Description",
                "class": "form-control auto-resize",
                "style": "height: 100px; position: relative;",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("description",)


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by task", "class": "form-control"}
        ),
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by worker", "class": "form-control"}
        ),
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )

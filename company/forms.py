from django import forms
from django.contrib.auth import get_user_model
from company.models import Task
from django.contrib.auth.forms import UserCreationForm


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
        widget=forms.TextInput(
            attrs={
                "placeholder": "Description",
                "class": "form-control",
                "style": "height: 100px;",
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


class TaskUpdateWorkersForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"style": "width: 20px; height: 20px;"}
        ),
    )

    class Meta:
        model = Task
        fields = ("assignees",)

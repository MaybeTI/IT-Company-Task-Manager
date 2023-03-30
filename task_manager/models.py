from django.db import models
from django.contrib.auth.models import AbstractUser
from it_company import settings


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    team_admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teams")


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="workers", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="workers", blank=True, null=True
    )

    def __str__(self):
        return self.username


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(max_length=255)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    def __str__(self):
        return self.name

from django.shortcuts import render
from django.views import generic
from task_manager.forms import (
    TaskForm,
    TaskUpdateWorkersForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    WorkerUpdateDescriptionForm,
)
from task_manager.models import Task
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, "company/index.html")


class TaskList(LoginRequiredMixin, generic.ListView):
    model = Task


class TaskDetail(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateWorkers(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateWorkersForm
    template_name = "company/task_detail.html"

    def get_success_url(self):
        return reverse_lazy("task_manager:task-detail", kwargs={"pk": self.request.user.id})


class WorkerList(LoginRequiredMixin, generic.ListView):
    model = get_user_model()


class WorkerDetail(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class WorkerCreate(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:index")


class WorkerUpdate(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateDescription(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateDescriptionForm
    template_name = "company/worker_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:worker-detail", kwargs={"pk": self.request.user.id}
        )

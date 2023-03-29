from django.shortcuts import render
from django.views import generic
from company.forms import TaskForm, TaskUpdateWorkersForm, WorkerCreateForm, WorkerUpdateForm
from company.models import Task
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


def index(request):
    return render(request, "company/index.html")


class TaskList(generic.ListView):
    model = Task


class TaskDetail(generic.DetailView):
    model = Task


class TaskCreate(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("company:task-list")


class TaskUpdate(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("company:task-list")


class TaskDelete(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("company:task-list")


class TaskUpdateWorkers(generic.UpdateView):
    model = Task
    form_class = TaskUpdateWorkersForm
    template_name = "company/task_detail.html"

    def get_success_url(self):
        return reverse_lazy("company:task-detail", kwargs={"pk": self.request.user.id})


class WorkerList(generic.ListView):
    model = get_user_model()


class WorkerDetail(generic.DetailView):
    model = get_user_model()


class WorkerCreate(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("company:index")


class WorkerUpdate(generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("company:worker-list")

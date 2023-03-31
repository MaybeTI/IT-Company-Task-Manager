from django.shortcuts import render
from django.views import generic
from task_manager.forms import (
    TaskForm,
    TaskUpdateWorkersForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    WorkerUpdateDescriptionForm,
    TaskSearchForm,
    WorkerSearchForm,
)
from task_manager.models import Task
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    user_tasks = request.user.tasks.select_related("task_type")
    context = {
        "user_tasks": user_tasks
    }
    return render(request, "task_manager/index.html", context=context)


class TaskList(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")

        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskDetail(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:task-detail", kwargs={"pk": self.kwargs["pk"]}
        )


class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateWorkers(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateWorkersForm
    template_name = "task_manager/task_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:task-detail", kwargs={"pk": self.kwargs["pk"]}
        )


class WorkerList(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = WorkerSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.select_related("position")

        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])

        return queryset


class WorkerDetail(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.select_related("position").prefetch_related("tasks")


class WorkerCreate(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:index")


class WorkerUpdate(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:worker-detail", kwargs={"pk": self.request.user.id}
        )


class WorkerUpdateDescription(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateDescriptionForm
    template_name = "task_manager/worker_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:worker-detail", kwargs={"pk": self.request.user.id}
        )

from django.urls import path

from company.views import index, TaskList, TaskDetail, TaskCreate, TaskUpdateWorkers, WorkerList

urlpatterns = [
    path("", index, name="index"),
    path("task-list/", TaskList.as_view(), name="task-list"),
    path("task/detail/<int:pk>/", TaskDetail.as_view(), name="task-detail"),
    path("task/create/", TaskCreate.as_view(), name="task-create"),
    path("task/update/<int:pk>/worker/", TaskUpdateWorkers.as_view(), name="task-update-workers"),
    path("worker-list/", WorkerList.as_view(), name="worker-list"),
]

app_name = "company"

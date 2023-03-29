from django.urls import path

from task_manager.views import (
    index,
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    TaskUpdateWorkers,
    WorkerList,
    WorkerDetail,
    WorkerCreate,
    WorkerUpdate,
    WorkerUpdateDescription,
)

urlpatterns = [
    path("", index, name="index"),
    path("task/list/", TaskList.as_view(), name="task-list"),
    path("task/detail/<int:pk>/", TaskDetail.as_view(), name="task-detail"),
    path("task/create/", TaskCreate.as_view(), name="task-create"),
    path("task/update/<int:pk>/", TaskUpdate.as_view(), name="task-update"),
    path("task/delete/<int:pk>/", TaskDelete.as_view(), name="task-delete"),
    path(
        "task/update/<int:pk>/worker/",
        TaskUpdateWorkers.as_view(),
        name="task-update-workers",
    ),
    path("worker/list/", WorkerList.as_view(), name="worker-list"),
    path("worker/detail/<int:pk>/", WorkerDetail.as_view(), name="worker-detail"),
    path("worker/create/", WorkerCreate.as_view(), name="worker-create"),
    path("worker/update/<int:pk>/", WorkerUpdate.as_view(), name="worker-update"),
    path(
        "worker/update/<int:pk>/description",
        WorkerUpdateDescription.as_view(),
        name="worker-update-description",
    ),
]

app_name = "task_manager"

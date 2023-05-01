from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.models import Position, Task, TaskType

TASK_LIST_URL = reverse("task_manager:task-list")
WORKER_LIST_URL = reverse("task_manager:worker-list")


def get_task_detail_url(pk: int):
    return reverse("task_manager:task-detail", kwargs={"pk": pk})


def get_worker_detail_url(pk: int):
    return reverse("task_manager:worker-detail", kwargs={"pk": pk})


class PublicViewTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="QA")
        self.worker = get_user_model().objects.create_user(
            username="test", password="test12345", position=self.position
        )
        self.task_type = TaskType.objects.create(name="QA")
        self.task = Task.objects.create(
            name="Task",
            description="some description",
            deadline=str(date.today() + timedelta(days=1)),
            is_completed=False,
            task_type=self.task_type,
        )


    def test_login_required_task_list(self):
        response = self.client.get(TASK_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2Ftask%2Flist%2F")

    def test_login_required_task_detail(self):
        response = self.client.get(get_task_detail_url(self.task.id))

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/detail/1/")

    def test_login_required_worker_list(self):
        response = self.client.get(WORKER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/worker/list/")

    def test_login_required_worker_detail(self):
        response = self.client.get(get_worker_detail_url(self.worker.id))

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/worker/detail/1/")


class PrivateViewTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="QA")
        self.worker = get_user_model().objects.create_user(
            username="test", password="test12345", position=self.position
        )
        self.client.force_login(self.worker)
        self.url = reverse("task_manager:task-create")

        self.task_type = TaskType.objects.create(name="QA")
        self.task = Task.objects.create(
            name="Task",
            description="some description",
            deadline=str(date.today() + timedelta(days=1)),
            is_completed=False,
            task_type=self.task_type,
        )

    def test_retrieve_task_list(self):
        query = Task.objects.all()
        response = self.client.get(TASK_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context.get("task_list")), list(query))
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_retrieve_worker_list(self):
        query = get_user_model().objects.all()
        response = self.client.get(WORKER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context.get("worker_list")), list(query))
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

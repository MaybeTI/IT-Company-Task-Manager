from django.test import TestCase
from task_manager.models import TaskType, Position, Task
from django.contrib.auth import get_user_model


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="test")
        self.position = Position.objects.create(name="test")
        self.worker1 = get_user_model().objects.create_user(
            username="BobKiller",
            password="test12345",
            position=self.position
        )
        self.worker2 = get_user_model().objects.create_user(
            username="MaxKiller",
            password="test12345",
            position=self.position
        )

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "test")

    def test_position_str(self):
        self.assertEqual(str(self.position), "test")

    def test_worker_str(self):
        self.assertEqual(str(self.worker1), "BobKiller")

    def test_task_str(self):
        task = Task.objects.create(
            name="Test task",
            deadline="2023-04-19",
            is_completed=False,
            priority="Low",
            task_type=self.task_type,
        )
        task.assignees.set([self.worker1, self.worker2])
        self.assertEqual(str(task), "Test task")

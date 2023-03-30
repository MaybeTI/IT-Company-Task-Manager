from django.test import TestCase
from task_manager.models import TaskType, Position, Task
from django.contrib.auth import get_user_model


class ModelsTest(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")
        self.assertEqual(str(task_type), "test")

    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), "test")

    def test_worker_str(self):
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username="BobKiller",
            password="test12345",
            position=position
        )
        self.assertEqual(str(worker), "BobKiller")

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test")
        position = Position.objects.create(name="test")
        worker1 = get_user_model().objects.create_user(
            username="BobKiller",
            password="test12345",
            position=position
        )
        worker2 = get_user_model().objects.create_user(
            username="MaxKiller",
            password="test12345",
            position=position
        )

        task = Task.objects.create(
            name="Test task",
            deadline="2023-04-19",
            is_completed=False,
            priority="Low",
            task_type=task_type,
        )
        task.assignees.set([worker1, worker2])
        self.assertEqual(str(task), "Test task")

from datetime import date, timedelta
from django.test import TestCase
from task_manager.models import Position, TaskType, Task
from task_manager.forms import WorkerCreateForm, WorkerUpdateForm, TaskForm, TaskUpdateWorkersForm
from django.contrib.auth import get_user_model


class WorkerFormsTests(TestCase):
    def setUp(self):
        self.position1 = Position.objects.create(name="QA")
        self.position2 = Position.objects.create(name="DevOps")
        self.form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "position": self.position1.id,
        }
        self.update_form_data = {
            "username": "usertest",
            "email": "testuser@exam.com",
            "position": self.position2.id
        }
        self.worker = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="mypassword",
            position=self.position1,
        )

    def test_worker_creation_form_with_valid_data(self):
        form = WorkerCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.position.name, "QA")

    def test_worker_creation_form_with_blank_form(self):
        form = WorkerCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_worker_creation_form_with_duplicate_username(self):
        form = WorkerCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_worker_creation_form_with_different_passwords(self):
        self.form_data["password2"] = "another_password"
        form = WorkerCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_worker_update_form_with_valid_data(self):
        form = WorkerUpdateForm(data=self.update_form_data, instance=self.worker)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "usertest")
        self.assertEqual(user.email, "testuser@exam.com")
        self.assertEqual(user.position.name, "DevOps")

    def test_worker_update_form_with_invalid_data(self):
        self.update_form_data["email"] = "test"
        form = WorkerUpdateForm(data=self.update_form_data)
        self.assertFalse(form.is_valid())


class TaskFormTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="QA")
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker1 = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="mypassword",
            position=self.position,
        )
        self.worker2 = get_user_model().objects.create_user(
            username="testusertest",
            email="testusertest@example.com",
            password="mypassword",
            position=self.position,
        )
        self.worker3 = get_user_model().objects.create_user(
            username="test",
            email="test@example.com",
            password="mypassword",
            position=self.position,
        )
        self.form_data = {
            "name": "Test task",
            "description": "Test description",
            "deadline": str(date.today() + timedelta(days=1)),
            "is_completed": False,
            "priority": "Low",
            "task_type": self.task_type,
            "assignees": [self.worker1.id, self.worker2.id]
        }
        self.update_form_data = {
            "name": "Task",
            "is_completed": True,
            "assignees": [self.worker1.id, self.worker2, self.worker3]
        }
        self.task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=str(date.today() + timedelta(days=1)),
            is_completed=False,
            priority="Low",
            task_type=self.task_type,
        )
        self.task.assignees.set([self.worker1.id, self.worker2.id])

    def test_task_form_with_valid_data(self):
        form = TaskForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.name, "Test task")
        self.assertEqual(task.deadline, date.today() + timedelta(days=1))

    def test_task_form_with_invalid_date(self):
        self.form_data["deadline"] = str(date.today() - timedelta(days=1))
        form = TaskForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_task_update_workers_form(self):
        form = TaskUpdateWorkersForm(data=self.update_form_data, instance=self.task)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertCountEqual(task.assignees.all(), [self.worker1, self.worker2, self.worker3])


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Dev")

        self.task_type = TaskType.objects.create(name="QA")

        self.worker1 = get_user_model().objects.create_user(
            username="BobKiller",
            email="testuser@example.com",
            password="mypassword",
            position=self.position,
        )

        self.worker2 = get_user_model().objects.create_user(
            username="next_legend",
            email="testusertest@example.com",
            password="mypassword",
            position=self.position,
        )

        self.worker3 = get_user_model().objects.create_user(
            username="top_jin",
            email="test@example.com",
            password="mypassword",
            position=self.position,
        )
        self.task1 = Task.objects.create(
            name="Professional task",
            description="Test description",
            deadline=str(date.today() + timedelta(days=1)),
            is_completed=False,
            priority="Low",
            task_type=self.task_type,
        )

        self.task2 = Task.objects.create(
            name="New task",
            description="Test description",
            deadline=str(date.today() + timedelta(days=1)),
            is_completed=False,
            priority="Low",
            task_type=self.task_type,
        )

        self.task3 = Task.objects.create(
            name="Task for jun",
            description="Test description",
            deadline=str(date.today() + timedelta(days=1)),
            is_completed=False,
            priority="Low",
            task_type=self.task_type,
        )

        self.client.force_login(self.worker1)

    def test_task_search_form(self):
        response = self.client.get("http://127.0.0.1:8000/task/list/?name=professional+task")

        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

        response = self.client.get("http://127.0.0.1:8000/task/list/?name=")

        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_worker_search_form(self):
        response = self.client.get("http://127.0.0.1:8000/worker/list/?username=killer")

        self.assertContains(response, self.worker1.username)
        self.assertNotContains(response, self.worker2.username)
        self.assertNotContains(response, self.worker3.username)

        response = self.client.get("http://127.0.0.1:8000/worker/list/?username=")

        self.assertContains(response, self.worker1.username)
        self.assertContains(response, self.worker2.username)
        self.assertContains(response, self.worker3.username)



from datetime import date, timedelta

from django.test import TestCase

from taskheat.core.factories import TaskFactory, CompletedTask


class SimpleTest(TestCase):
    def test_max_weight_temperature_calculation(self):
        task = TaskFactory.build(max_weight=5)
        completed_task = CompletedTask.build(task=task, weight=5)

        self.assertEqual(task.temperature_calculation(date.today(),
                                                      completed_task),
                         task.max_weight)

    def test_partial_weight_temperature_calculation(self):
        task = TaskFactory.build(max_weight=10)
        completed_task = CompletedTask.build(task=task, weight=5)

        self.assertEqual(task.temperature_calculation(date.today(),
                                                      completed_task),
                         completed_task.weight)

    def test_negative_weight_temperature_calculation(self):
        task = TaskFactory.build(min_weight=-10)
        completed_task = CompletedTask.build(task=task, weight=-1)

        self.assertEqual(task.temperature_calculation(date.today(),
                                                      completed_task),
                         completed_task.weight)

    def test_positive_partially_decayed_temperature_calculation(self):
        days_ago = 3
        start_date = date.today() - timedelta(days=days_ago)
        start = 5

        task = TaskFactory.build(max_weight=10, min_weight=-10,
                                 decay_interval=-1)
        completed_task = CompletedTask.build(when=start_date, task=task,
                                             weight=start)

        self.assertEqual(task.temperature_calculation(date.today(),
                                                      completed_task),
                         start-days_ago)

    def test_negative_partially_decayed_temperature_calculation(self):
        days_ago = 8
        start_date = date.today() - timedelta(days=days_ago)
        start = 5

        task = TaskFactory.build(max_weight=10, min_weight=-10,
                                 decay_interval=-1)
        completed_task = CompletedTask.build(when=start_date, task=task,
                                             weight=start)

        self.assertEqual(task.temperature_calculation(date.today(),
                                                      completed_task),
                         start-days_ago)

    def test_positive_decay_rate_temperature_calculation(self):
        days_ago = 3
        start_date = date.today() - timedelta(days=days_ago)
        start = 5

        task = TaskFactory.build(max_weight=10, min_weight=-10,
                                 decay_interval=1)
        completed_task = CompletedTask.build(when=start_date, task=task,
                                             weight=start)

        self.assertEqual(task.temperature_calculation(date.today(),
                                                      completed_task),
                         start+days_ago)

from datetime import date, timedelta

from django.test import TestCase

from taskheat.core.factories import TaskFactory, CompletedTaskFactory


one_day = timedelta(days=1)
today = date.today()
week_ago = today - (one_day*7)

class SimpleTest(TestCase):
    def test_max_weight_temperature_calculation(self):
        task = TaskFactory.build(max_weight=5)
        completed_task = CompletedTaskFactory.build(task=task, weight=5)

        self.assertEqual(
            task.temperature_calculation(start=week_ago, end=today,
                                         completed_task_list=(completed_task,)),
            [0,0,0,0,0,0,task.max_weight])

    def test_partial_weight_temperature_calculation(self):
        task = TaskFactory.build(max_weight=10)
        completed_task = CompletedTaskFactory.build(task=task, weight=5)

        self.assertEqual(task.temperature_calculation(today,
                                                      completed_task),
                         completed_task.weight)

    def test_negative_weight_temperature_calculation(self):
        task = TaskFactory.build(min_weight=-10)
        completed_task = CompletedTaskFactory.build(task=task, weight=-1)

        self.assertEqual(task.temperature_calculation(today,
                                                      completed_task),
                         completed_task.weight)

    def test_positive_partially_decayed_temperature_calculation(self):
        days_ago = 3
        start_date = today - timedelta(days=days_ago)
        start = 5

        task = TaskFactory.build(max_weight=10, min_weight=-10,
                                 decay_interval=-1)
        completed_task = CompletedTaskFactory.build(when=start_date,
                                                    task=task, weight=start)

        self.assertEqual(task.temperature_calculation(today,
                                                      completed_task),
                         start-days_ago)

    def test_negative_partially_decayed_temperature_calculation(self):
        days_ago = 8
        start_date = today - timedelta(days=days_ago)
        start = 5

        task = TaskFactory.build(max_weight=10, min_weight=-10,
                                 decay_interval=-1)
        completed_task = CompletedTaskFactory.build(when=start_date,
                                                    task=task, weight=start)

        self.assertEqual(task.temperature_calculation(today,
                                                      completed_task),
                         start-days_ago)

    def test_positive_decay_rate_temperature_calculation(self):
        days_ago = 3
        start_date = today - timedelta(days=days_ago)
        start = 5

        task = TaskFactory.build(max_weight=10, min_weight=-10,
                                 decay_interval=1)
        completed_task = CompletedTaskFactory.build(when=start_date,
                                                    task=task, weight=start)

        self.assertEqual(task.temperature_calculation(today,
                                                      completed_task),
                         start+days_ago)

    def test_aggregate_completed_tasks(self):
        task = TaskFactory.build(max_weight=10)
        completed_task_1 = CompletedTaskFactory.build(task=task, weight=5)
        completed_task_2 = CompletedTaskFactory.build(task=task, weight=3)

        self.assertEqual(task.temperature_calculation(today,
                                                      [completed_task_1,
                                                       completed_task_2]),
                         completed_task_1.weight+completed_task_2.weight)

    def test_aggregates_respect_max_weight(self):
        task = TaskFactory.build(max_weight=10)
        completed_task_1 = CompletedTaskFactory.build(task=task, weight=5)
        completed_task_2 = CompletedTaskFactory.build(task=task, weight=8)

        self.assertEqual(task.temperature_calculation(today,
                                                      [completed_task_1,
                                                       completed_task_2]),
                         task.max_weight)

    def test_aggregates_respect_max_weight_for_day_when_decaying(self):
        yesterday = today - one_day
        task = TaskFactory.build(max_weight=10)
        completed_task_1 = CompletedTaskFactory.build(when=yesterday,
                                                      task=task, weight=5)
        completed_task_2 = CompletedTaskFactory.build(when=yesterday,
                                                      task=task, weight=8)

        self.assertEqual(task.temperature_calculation(today,
                                                      [completed_task_1,
                                                       completed_task_2]),
                         task.max_weight+task.decay_interval)

    def test_proper_decay_for_completion_on_different_days(self):
        today = today
        one_day = one_day
        task = TaskFactory.build(max_weight=10)
        completed_task_1 = CompletedTaskFactory.build(when=today-(2*one_day),
                                                      task=task, weight=5)
        completed_task_2 = CompletedTaskFactory.build(when=today-(3*one_day),
                                                      task=task, weight=6)

        self.assertEqual(task.temperature_calculation(today,
                                                      [completed_task_1,
                                                       completed_task_2]),
                         8)
        self.assertEqual(task.temperature_calculation(today-one_day,
                                                      [completed_task_1,
                                                       completed_task_2]),
                         9)
        self.assertEqual(task.temperature_calculation(today-(2*one_day),
                                                      [completed_task_1,
                                                       completed_task_2]),
                         10)
        self.assertEqual(task.temperature_calculation(today-(3*one_day),
                                                      [completed_task_1,
                                                       completed_task_2]),
                         6)

    def test_for_proper_weight_after_decay_bottoms_for_one_completion(self):
        today = today
        one_day = one_day
        task = TaskFactory.build(max_weight=10, min_weight=-1)
        completed_task_1 = CompletedTaskFactory.build(when=today-(2*one_day),
                                                      task=task, weight=4)
        completed_task_2 = CompletedTaskFactory.build(when=today-(5*one_day),
                                                      task=task, weight=1)

        self.assertEqual(task.temperature_calculation(today,
                                                      [completed_task_1,
                                                       completed_task_2]),
                         8)
        self.assertEqual(task.temperature_calculation(today-one_day,
                                                      [completed_task_1,
                                                       completed_task_2]),
                         9)
        self.assertEqual(task.temperature_calculation(today-(2*one_day),
                                                      [completed_task_1,
                                                       completed_task_2]),
                         10)
        self.assertEqual(task.temperature_calculation(today-(3*one_day),
                                                      [completed_task_1,
                                                       completed_task_2]),
                         6)
        self.assertEqual(task.temperature_calculation(today-(4*one_day),
                                                      [completed_task_1,
                                                       completed_task_2]),
                         6)
        self.assertEqual(task.temperature_calculation(today-(5*one_day),
                                                      [completed_task_1,
                                                       completed_task_2]),
                         6)

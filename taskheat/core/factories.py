from datetime import date

from factory import Factory, LazyAttribute

from taskheat.core.models import Task, CompletedTask


class TaskFactory(Factory):
    FACTORY_FOR = Task

    name = 'Shower'
    details = 'Took a shower'
    max_weight = 2
    min_weight = -10
    decay_interval = -1


class CompletedTaskFactory(Factory):
    FACTORY_FOR = CompletedTask

    task = LazyAttribute(lambda a: TaskFactory.build())
    weight = 2
    when = LazyAttribute(lambda a: date.today())
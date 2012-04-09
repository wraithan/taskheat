from datetime import date, timedelta

from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    max_weight = models.IntegerField()
    min_weight = models.IntegerField()
    decay_interval = models.IntegerField()
    owner = models.ForeignKey('auth.User')

    def temperature(self, when=None):
        when = when or date.today()
        completed_task_list = self.completedtask_set.filter().order_by('-when')

        if completed_task_list.exists():
            completed_task = completed_task_list[0]
        else:
            completed_task = None
        return self.temperature_calculation(when, completed_task)


    def temperature_calculation(self, when, completed_task):
        if completed_task:
            today = date.today()
            days_old = (today-completed_task.when).days
            decayed_amount = (completed_task.weight
                              + (days_old
                                 * self.decay_interval))
            if self.decay_interval > 0:
                if decayed_amount < self.max_weight:
                    return decayed_amount
                else:
                    return self.max_weight
            else:
                if decayed_amount > self.min_weight:
                    return decayed_amount
                else:
                    return self.min_weight
        else:
            if self.decay_interval > 0:
                return self.max_weight
            else:
                return self.min_weight

    def __unicode__(self):
        return "%s (%d)" % (self.name, self.temperature(date.today()))

class CompletedTask(models.Model):
    task = models.ForeignKey('Task')
    weight = models.IntegerField()
    when = models.DateField(default=date.today)

    def __unicode__(self):
        return "%d of %s on %s" % (self.weight,
                                   self.task.name,
                                   self.when)

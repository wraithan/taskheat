from datetime import date, timedelta

from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    max_weight = models.IntegerField()
    min_weight = models.IntegerField()
    decay_interval = models.IntegerField()

    def temperature(self, when):
        possible_completed_task = self.completedtask_set.filter(
            when__gte=start).order_by('-when')

        if possible_completed_task.exists():
            completed_task = possible_greens[0]
        else:
            completed_task = None
        return self.temperature_calculation(when, completed_task)


    def temperature_calculation(self, when, completed_task):
        if completed_task:
            today = date.today()
            start = today-timedelta(days=self.max_weight+-self.min_weight)
            days_old = (today-completed_task.when).days
            decayed_value = (completed_task.weight
                             + (days_old
                                * self.decay_interval))
            if self.decay_interval > 0:
                if decayed_value < self.max_weight:
                    return decayed_value
                else:
                    return self.max_weight
            else:
                if decayed_value > self.min_weight:
                    return decayed_value
                else:
                    return self.min_weight
        else:
            if self.decay_interval > 0:
                return self.max_weight
            else:
                return self.min_weight


class CompletedTask(models.Model):
    task = models.ForeignKey('Task')
    weight = models.IntegerField()
    when = models.DateField(auto_now_add=True)

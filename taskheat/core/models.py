from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    max_weight = models.IntegerField()
    min_weight = models.IntegerField()
    decay_interval = models.IntegerField()

    def temperature(self, when):
        today = date.today()
        start = today-timedelta(days=self.max_weight+-self.min_weight)
        possible_ct = self.completedtask_set.filter(when__gte=start).order_by('-when')
        if possible_ct.exists():
            ct = possible_greens[0]
            days_old = (today-ct.when).days
            decayed_value = ct.weight + days_old*self.decay_interval
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

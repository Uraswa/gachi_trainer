from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=256)
    weekDays = models.CharField(max_length=999) # через запятую индексы дней недели. 0,2,5,6

    def __str__(self):
        return self.name

# password = admin, name = admin
class CollectionModel(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, related_name="collections", null=True)
    name = models.CharField(max_length=256, default="")
    short_name = models.CharField(max_length=256, unique=True, null=False)
    task_intervals = models.CharField(max_length=256, default="")
    avg_cost = models.DecimalField(default=1, decimal_places=1, max_digits=2)
    priority = models.IntegerField(default=1)
    enabled = models.BooleanField(default=True)
    description = models.TextField(null=True,default="")
    limit = models.IntegerField(default=9999)

    def __unicode__(self):
        return u'%s' % (self.name)

    def __str__(self):
        return self.name


class TaskModel(models.Model):
    collection = models.ForeignKey(to=CollectionModel, on_delete=models.CASCADE, related_name="tasks")
    task_name = models.CharField(max_length=256, unique=True, null=False)
    task_cost = models.DecimalField(default=1, decimal_places=1, max_digits=2)
    task_repeat_in_index = models.IntegerField(default=0)
    task_repeat_date = models.DateField()
    description = models.TextField(null=True, default="")
    banned = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.task_name}({self.task_cost})"


    def getDays(self):
        if self.task_repeat_in_index == 0: return 2
        if self.task_repeat_in_index == 1: return 3
        if self.task_repeat_in_index == 2: return 7
        if self.task_repeat_in_index == 3: return 14
        if self.task_repeat_in_index == 4: return 21
        if self.task_repeat_in_index == 5: return 28
        return 7



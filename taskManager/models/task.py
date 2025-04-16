from django.db import models
from base.models.base import ModelAbstractBase


class Task(ModelAbstractBase):

    status_choice = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    task = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=status_choice)
    assignee = models.CharField(max_length=50)
    due_date = models.DateField()
    source = models.CharField(max_length=20,blank=True)

    def __str__(self):
        # return super().__str__()
        return f"{self.task} : {self.status}"

    @classmethod
    def get_task_obj(cls,**criteria):
        return Task.objects.get(**criteria)

    @classmethod
    def get_task_queryset(cls,**criteria):
        return Task.objects.filter(**criteria)

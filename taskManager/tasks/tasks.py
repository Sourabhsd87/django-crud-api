from celery import shared_task
import csv
from io import StringIO
from taskManager.models.task import Task

@shared_task
def create_tasks_from_csv(decoded_lines):
    print("===================")
    file = StringIO("\n".join(decoded_lines))
    reader = csv.DictReader(file)

    for row in reader:
        Task.objects.create(
            task=row["task"],
            description=row["description"],
            status=row["status"],
            assignee=row["assignee"],
            due_date=row["due_date"],
            source="csv"
        )

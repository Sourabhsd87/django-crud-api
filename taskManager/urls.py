from django.urls import path
from taskManager.views.task import PingAPIView, TaskListAPIView, TaskCreateAPIView, TaskUpdateAPIView, TaskDeleteAPIView, BulkTaskUploadAPIView

urlpatterns = [
    path(
        "tasks/ping",
        PingAPIView.as_view(),
        name="task-ping"  
    ),
    path(
        "tasks",
        TaskListAPIView.as_view(), 
        name="task-list"),
    path(
        "task/create",
        TaskCreateAPIView.as_view(),
        name="task-create"),
    path(
        "task/update/<uuid:internal_id>",
        TaskUpdateAPIView.as_view(),
        name="task-update"),
    path(
        "tasks/delete",
        TaskDeleteAPIView.as_view(),
        name="task-delete"),
    path(
        "tasks/bulk-upload/",
        BulkTaskUploadAPIView.as_view(),
        name="bulk-task-upload"
        ),
]

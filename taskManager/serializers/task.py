import logging
from rest_framework import serializers
from django.utils.dateparse import parse_date
from taskManager.models.task import Task
from django.db.models import Q
import csv
from taskManager.tasks.tasks import create_tasks_from_csv
from mysite.settings import BASE_DIR

logger = logging.getLogger("taskManager")
print(BASE_DIR)
# from taskManager.serializers import (
#     TaskModelSerializer,
# )  # assume you already have this for output


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "internal_id",
            "task",
            "description",
            "status",
            "assignee",
            "due_date",
        ]


class TaskListSerializer(serializers.Serializer):
    
    def getTaskData(**criteria):
        logger.debug(f"[TaskListSerializer] Fetching tasks with criteria: {criteria}")
        return Task.get_task_queryset(**criteria)

    def filterTaskData(self, data):
        request = self.context["request"]
        logger.debug("[TaskListSerializer] Starting tasks filtering process")

        # Search filter
        search = request.GET.get("search")
        if search:
            logger.debug(f"[TaskListSerializer] Applying search filter: {search}")
            return data.filter(
                Q(task__icontains=search) |
                Q(description__icontains=search) |
                Q(assignee__icontains=search)
            )

        # Sorting
        sort_by = request.GET.get("sort_by", "created_on")
        order = request.GET.get("order", "desc")
        logger.debug(f"[TaskListSerializer] Sorting by: {sort_by}, Order: {order}")

        if order == "asc":
            sort_by = f"-{sort_by}"
            logger.debug(f"[TaskListSerializer] Reversed sorting: {sort_by}")

        data = data.order_by(sort_by)
        logger.debug(f"[TaskListSerializer] Applied ordering on: {sort_by}")

        # Filters
        status_filter = request.GET.get("status")
        assignee_filter = request.GET.get("assignee")
        due_date_filter = request.GET.get("due_date")

        if status_filter:
            logger.debug(f"[TaskListSerializer] Applying status filter: {status_filter}")
            data = data.filter(status__icontains=status_filter)

        if assignee_filter:
            logger.debug(f"[TaskListSerializer] Applying assignee filter (icontains): {assignee_filter}")
            data = data.filter(assignee__icontains=assignee_filter)

        if due_date_filter:
            parsed_due_date = parse_date(due_date_filter)
            if parsed_due_date:
                logger.debug(f"[TaskListSerializer] Applying due_date filter: {parsed_due_date}")
                data = data.filter(due_date=parsed_due_date)
            else:
                logger.warning(f"[TaskListSerializer] Invalid due_date format provided: {due_date_filter}")

        logger.debug("[TaskListSerializer] Finished filtering tasks")
        return data

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "task",
            "description",
            "status",
            "assignee",
            "due_date",
            "is_active",
        ]

    def create(self, validated_data):
        validated_data["source"] = "api"
        task_obj = Task.objects.create(**validated_data)
        return task_obj

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "task",
            "description",
            "status",
            "assignee",
            "due_date",
            "is_active",
        ]
        
    def validate(self, attrs):
        # return super().validate(attrs)
        try:
            self.instance = Task.get_task_obj(internal_id=self.context.get('internal_id'))
        except Task.DoesNotExist:
            raise serializers.ValidationError("Task with this ID does not exist")
        return attrs        
        

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class TaskDeleteSerializer(serializers.Serializer):
    internal_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        help_text="List of internal_ids to delete"
    )

    def validate_internal_ids(self, value):
        existing_tasks = Task.objects.filter(internal_id__in=value)
        if not existing_tasks.exists():
            raise serializers.ValidationError("No tasks found for given IDs.")
        self.existing_tasks = existing_tasks
        return value

    def delete_tasks(self):
        deleted_count, _ = self.existing_tasks.delete()
        return deleted_count
    
class BulkTaskUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, file):
        # Check MIME type and file extension
        allowed_mime_types = ['text/csv']
        allowed_extensions = ['.csv']

        file_mime_type = file.content_type
        file_extension = file.name.lower().rsplit('.', 1)[-1] if '.' in file.name else ''

        if file_mime_type not in allowed_mime_types or f".{file_extension}" not in allowed_extensions:
            raise serializers.ValidationError(
                f"Invalid file type. Must be a CSV. Detected MIME type: {file_mime_type}"
            )

        # if file.size > 2 * 1024 * 1024:  # Optional: limit size to 2MB
        #     raise serializers.ValidationError("File is too large. Max size allowed is 2MB.")

        return file

    def validate(self, attrs):
        csv_file = attrs.get("file")
        
        try:
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            required_headers = {"task", "description", "status", "assignee", "due_date"}
            print(reader.fieldnames)
            if not required_headers.issubset(reader.fieldnames):
                raise serializers.ValidationError(
                    {"file": f"CSV must contain headers: {required_headers}"}
                )

            # Save the decoded CSV lines for use in create()
            self.decoded_file = decoded_file

        except Exception as e:
            raise serializers.ValidationError({"file": f"Invalid file or format: {str(e)}"})

        return attrs

    def create(self, validated_data):
        # Send decoded CSV data to celery
        print("---------------")
        create_tasks_from_csv.delay(self.decoded_file)
        return validated_data
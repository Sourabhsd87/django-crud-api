from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from mysite.settings import BASE_DIR
from taskManager.serializers.task import (
    TaskListSerializer,
    TaskModelSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskDeleteSerializer,
    BulkTaskUploadSerializer,
    
)
import csv
from taskManager.tasks.tasks import create_tasks_from_csv

class PingAPIView(APIView):
    def get(self, request):
        print(BASE_DIR)
        return Response(status=status.HTTP_200_OK)

class TaskListAPIView(APIView):
    serializer_class = TaskListSerializer

    def get(self, request):
        serializer = self.serializer_class(context={"request": request})
        taskData = self.serializer_class.getTaskData()
        filtered_queryset = serializer.filterTaskData(taskData)
        response = TaskModelSerializer(filtered_queryset, many=True)
        return Response(response.data, status=status.HTTP_200_OK)


class TaskCreateAPIView(APIView):
    serializer_class = TaskCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            created_task = serializer.save()
            response = TaskModelSerializer(created_task)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskUpdateAPIView(APIView):
    serializer_class = TaskUpdateSerializer

    def put(self, request, internal_id):

        serializer = self.serializer_class(data=request.data, context={"internal_id": internal_id})
        if serializer.is_valid():
            updated_task = serializer.save()
            response = TaskModelSerializer(updated_task)
            return Response(response.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDeleteAPIView(APIView):
    serializer_class = TaskDeleteSerializer

    def delete(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            deleted_count = serializer.delete_tasks()
            return Response(
                {"message": f"Successfully deleted {deleted_count} tasks."},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )
        
class BulkTaskUploadAPIView(APIView):
    parser_classes = [MultiPartParser]
    serializer_class = BulkTaskUploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Task creation started in background."}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

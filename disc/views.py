from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Description, RateBy, Desc_RateBy, WarehouseActivity
from .serializer import (
    DescriptionCreateSeriaizer,
    DescriptionUpdateSerializer,
    RateByCreateSerializer,
    RateByUpdateSerializer,
    RateByListSerializer,
    DescRateByCreateSerializer,
    DescRateByUpdateSerializer,
    DescriptionListSerializer,
    WarehouseActivityListSerializer,
)
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date


# Create your views here.
class DescriptionListAPIView(APIView):
    def get(self, request):
        description = Description.objects.all()
        serializer = DescriptionListSerializer(description, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DescriptionCreateAPIView(APIView):
    def post(self, request):
        serializer = DescriptionCreateSeriaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DescriptionUpdateAPIView(APIView):
    def put(self, request, pk):
        # description = get_object_or_404(Description, pk=pk)
        description = Description.objects.filter(internal_id=pk).first()
        if not description:
            return Response(
                {"error": f"Description with ID {pk} does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = DescriptionUpdateSerializer(
            description, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DescriptionDeleteAPIView(APIView):
    def delete(self, request, pk):
        # description = get_object_or_404(Description, pk=pk)
        description = Description.objects.filter(internal_id=pk).first()
        if not description:
            return Response(
                {"error": f"Description with ID {pk} does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        description.delete()
        return Response(
            {"message": "Description deleted successsfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class RateByListAPIView(APIView):
    def get(self, request):
        ratebys = RateBy.objects.all()
        serializer = RateByListSerializer(ratebys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RateByCreateAPIView(APIView):
    def post(self, request):
        serializer = RateByCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RateByUpdateAPIView(APIView):
    def put(self, request, pk):
        # rateBy = get_object_or_404(RateBy, pk=pk)
        rateBy = RateBy.objects.filter(internal_id=pk).first()
        if not rateBy:
            return Response(
                {"error": f"Rateby with ID {pk} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RateByUpdateSerializer(
            rateBy, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


class RateByDeleteAPIView(APIView):
    def delete(self, request, pk):
        # rateBy = get_object_or_404(RateBy, pk=pk)
        rateBy = RateBy.objects.filter(internal_id=pk).first()
        if not rateBy:
            return Response(
                {"error": f"RateBy eith ID {pk} does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        rateBy.delete()
        return Response(
            {"message": "RateBy deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class DescRateByCreateAPIView(APIView):
    def post(self, request):

        description_id = request.data.get("description")

        if not Description.objects.filter(internal_id=description_id).exists():
            return Response(
                {"error": f"Description with ID {description_id} does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DescRateByCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DescRateByUpdateAPIView(APIView):
    def put(self, request, description_id):
        description = Description.objects.filter(internal_id=description_id).first()
        if not description:
            return Response(
                {"error": f"Description with ID {description_id} does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        desc_rateby = Desc_RateBy.objects.filter(
            description__internal_id=description.internal_id
        ).first()
        if not desc_rateby:
            return Response(
                {
                    "error": f"RateBys for description with ID {description_id} does not exist."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = DescRateByUpdateSerializer(
            desc_rateby, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListRatebysByDescriptionAPIView(APIView):
    def get(self, request, description_id):

        # try:
        #     desc_rateby = Desc_RateBy.objects.get(internal_id=description_id)
        #     ratebys = desc_rateby.rateBy.all()

        # except Desc_RateBy.DoesNotExist:
        #     return Response(
        #         {"error": "Description not found or has no ratebys"},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )
        description = Description.objects.filter(internal_id=description_id).first()
        if not description:
            return Response(
                {"error": f"Description with ID {description_id} does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            desc_rateby = Desc_RateBy.objects.get(description=description.pk)
        except Desc_RateBy.DoesNotExist:
            return Response(
                {"error": f"No RateBy data found for Description ID {description_id}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ratebys = desc_rateby.rateBy.all()

        serializer = RateByListSerializer(ratebys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListWarehouseActivityAPIView(APIView):

    serializer_class = WarehouseActivityListSerializer

    def get(self, request):

        queryset = WarehouseActivity.get_warehouse_activity_queryset()
        serializer = self.serializer_class(context={"request": request})
        filtered_queryset = serializer.filter_data(data=queryset)
        response = WarehouseActivityListSerializer(filtered_queryset, many=True)
        return Response(response.data, status=status.HTTP_200_OK)

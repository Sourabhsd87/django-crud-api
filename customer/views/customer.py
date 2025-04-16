from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customer.models.customer import Customer
from customer.serializers.customer import (
    CustomerListSerializer,
    CustomerModelSerializer,
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
)


class CustomerListAPIView(APIView):

    serializer_class = CustomerListSerializer

    def get(self, request):
        serializer = self.serializer_class(context={"request": request})
        customerData = serializer.getcustomerData()
        filtered_queryset = serializer.filterCustomerData(data=customerData)
        response = CustomerModelSerializer(filtered_queryset, many=True)
        return Response(response.data, status=status.HTTP_200_OK)


class CustomerCreateAPIView(APIView):

    serializer_class = CustomerCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            response = CustomerModelSerializer(customer)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerUpdateAPIView(APIView):
    serializer_class = CustomerUpdateSerializer

    def put(self, request, internal_id):
        serializer = self.serializer_class(
            data=request.data, context={"internal_id": internal_id}
        )
        if serializer.is_valid():
            updated_customer = serializer.save()
            response = CustomerModelSerializer(updated_customer)
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, internal_id):
        # Pass the internal_id as context and use partial=True for PATCH
        serializer = self.serializer_class(
            data=request.data, context={"internal_id": internal_id}, partial=True
        )

        if serializer.is_valid():
            updated_customer = serializer.save()
            response = CustomerModelSerializer(updated_customer)
            return Response(response.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDeleteAPIView(APIView):
    def delete(self, request, internal_id):
        try:
            customer = Customer.get_customer_obj(internal_id=internal_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": f"Customer with ID {internal_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        customer.delete()
        return Response(
            {"message": f"Customer with ID {internal_id} deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

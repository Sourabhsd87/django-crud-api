from rest_framework import serializers
from customerorder.models.order import Order


class OrderModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["order_id", "order_date", "status", "total_amount"]


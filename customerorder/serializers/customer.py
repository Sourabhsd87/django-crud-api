from rest_framework import serializers
from django.utils import timezone
from django.utils.dateparse import parse_date
from customerorder.models import Customer


class CustomerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["internal_id", "name", "email", "phone"]


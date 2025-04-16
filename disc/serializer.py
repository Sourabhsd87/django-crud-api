from rest_framework import serializers
from .models import Description, RateBy, Desc_RateBy, WarehouseActivity
from django.utils import timezone
from django.utils.dateparse import parse_date
import logging

logger = logging.getLogger("description")


class DescriptionListSerializer(serializers.ModelSerializer):
    logger.debug("In desc list serializer")
    description_name = serializers.CharField(source="value")

    class Meta:
        model = Description
        fields = ["internal_id", "description_name"]


class DescriptionCreateSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ["slug", "value"]


class DescriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = [
            "slug",
            "value",
        ]

    def update(self, instance, validated_data):
        # print(validated_data)

        instance.slug = validated_data.get("slug")
        instance.value = validated_data.get("value")

        instance.updated_at = timezone.now()
        instance.save()
        # print(instance.slug, instance.value)
        return instance


class RateByListSerializer(serializers.ModelSerializer):

    rateby_name = serializers.CharField(source="value")

    class Meta:
        model = RateBy
        fields = ["internal_id", "rateby_name"]


class RateByCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateBy
        fields = ["slug", "value"]


class RateByUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateBy
        fields = ["slug", "value"]

    def update(self, instance, validated_data):

        instance.slug = validated_data.get("slug")
        instance.value = validated_data.get("value")
        instance.updated_at = timezone.now()

        instance.save()

        return instance


class DescRateByCreateSerializer(serializers.ModelSerializer):

    rateBy = serializers.PrimaryKeyRelatedField(
        queryset=RateBy.objects.all(), many=True
    )

    class Meta:
        model = Desc_RateBy
        fields = ["description", "rateBy"]

    def create(self, validated_data):
        rateBy_data = validated_data.pop("rateBy")

        desc_rateby = Desc_RateBy.objects.create(**validated_data)
        desc_rateby.rateBy.set(rateBy_data)

        return desc_rateby


class DescRateByUpdateSerializer(serializers.ModelSerializer):
    rateBy = serializers.PrimaryKeyRelatedField(
        queryset=RateBy.objects.all(), many=True
    )

    class Meta:
        model = Desc_RateBy
        fields = ["rateBy"]

    def update(self, instance, validated_data):

        if "rateBy" in validated_data:
            instance.rateBy.set(validated_data["rateBy"])
        instance.save()
        return instance


class WarehouseActivityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseActivity
        fields = [
            "internal_id",
            "activity_id",
            "activity_type",
            "warehouse_number",
            "company_number",
            "purchase_order",
            "uom",
            "wh_pull_date",
        ]

    def filter_data(self, data):
        request = self.context["request"]

        activity_type_filter = request.GET.get("activity_type")
        uom_filter = request.GET.get("uom")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if activity_type_filter:
            data = data.filter(activity_type=activity_type_filter)

        if uom_filter:
            data = data.filter(uom=uom_filter)

        if start_date and end_date:
            # Convert to proper date objects
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if start_date and end_date:
                data = data.filter(wh_pull_date__date__range=(start_date, end_date))
        elif start_date:
            start_date = parse_date(start_date)
            if start_date:
                data = data.filter(wh_pull_date__date__gte=start_date)
        elif end_date:
            end_date = parse_date(end_date)
            if end_date:
                data = data.filter(wh_pull_date__date__lte=end_date)
        
        return data

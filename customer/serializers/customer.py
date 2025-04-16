from rest_framework import serializers
from customer.models.customer import Customer
from django.utils.dateparse import parse_date


class CustomerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            "internal_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "is_active",
        ]


class CustomerListSerializer(serializers.Serializer):

    def getcustomerData(self, **criteria):
        return Customer.get_customer_queryset(**criteria)

    def filterCustomerData(self, data):
        request = self.context["request"]

        country_filter = request.GET.get("country")
        status_filter = request.GET.get("status")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if country_filter:
            data = data.filter(country=country_filter)

        if status_filter:
            status = data.filter(status=status_filter)

        if start_date and end_date:
            # Convert to proper date objects
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if start_date and end_date:
                data = data.filter(dob__date__range=(start_date, end_date))
        elif start_date:
            start_date = parse_date(start_date)
            if start_date:
                data = data.filter(dob__date__gte=start_date)
        elif end_date:
            end_date = parse_date(end_date)
            if end_date:
                data = data.filter(dob__date__lte=end_date)

        return data


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "dob",
        ]

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "dob",
            "is_active"
        ]
        
    def validate(self, attrs):
        internal_id = self.context.get('internal_id')
        try:
            self.instance = Customer.get_customer_obj(internal_id=internal_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer with this internal ID does not exist.")
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


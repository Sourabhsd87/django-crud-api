from django.db import models
from base.models.base import ModelAbstractBase


class Customer(ModelAbstractBase):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        # return super().__str__()
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_customer_obj(**criteria):
        return Customer.objects.get(**criteria)

    @classmethod
    def get_customer_queryset(**criteria):
        return Customer.objects.filter(**criteria)

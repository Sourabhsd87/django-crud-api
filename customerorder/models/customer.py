from django.db import models
from base.models.base import ModelAbstractBase


class Customer(ModelAbstractBase):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def get_customer_obj(cls, **criteria):
        """
        returns Customer object
        """
        return Customer.objects.get(**criteria)

    def get_customer_queryset(cls, **criteria):
        """
        returns Customer queryset
        """
        return Customer.objects.filter(**criteria)

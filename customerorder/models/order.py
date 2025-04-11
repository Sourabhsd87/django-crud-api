from django.db import models
from base.models.base import ModelAbstractBase
from .customer import Customer


class Order(ModelAbstractBase):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    order_id = models.CharField(max_length=50, unique=True)
    order_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order_id} : {self.customer.name}"

    def get_order_obj(cls,**criteria):
        """
        returns order object
        """
        return Order.objects.get(**criteria)
    
    def get_order_queryset(cls, **criteria):
        """
        returns order queryset
        """
        return Order.objects.filter(**criteria)
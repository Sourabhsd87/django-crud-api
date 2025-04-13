from django.db import models
from base.models.base import ModelAbstractBase

class PurchaseOrder(ModelAbstractBase):
    purchase_order = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    suffix = models.CharField(max_length=5)
    company = models.CharField(max_length=20)
    warehouse = models.CharField(max_length=20)
    carrier = models.CharField(max_length=50, blank=True, null=True)
    services = models.CharField(max_length=100, blank=True, null=True)
    pro_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.purchase_order} - {self.company}"
    
    def get_purchaseOrder_obj(**criteria):
        return PurchaseOrder.objects.get()
    
    def get_purchaseOrder_queryset(**criteria):
        return PurchaseOrder.objects.filter(**criteria)
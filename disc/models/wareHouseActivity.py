from django.db import models
from base.models.base import ModelAbstractBase


class WarehouseActivity(ModelAbstractBase):

    activity_id = models.CharField(max_length=50, unique=True)
    activity_type = models.CharField(max_length=50)
    warehouse_number = models.CharField(max_length=20)
    company_number = models.IntegerField()
    purchase_order = models.CharField(max_length=20)
    uom = models.CharField(max_length=50)
    wh_pull_date = models.DateTimeField()

    def __str__(self):
        return f"Activity Id : {self.activity_id}\nActivity Type : {self.activity_type}"

    @classmethod
    def get_warehouse_activity_obj(cls, **criteria):
        """
        Returns object
        """
        return cls.objects.get(**criteria)

    @classmethod
    def get_warehouse_activity_queryset(cls, **criteria):
        """
        Returns queryset
        """
        return cls.objects.filter(**criteria)

from django.db import models
from django.utils import timezone
from .description import Description
from .rateBy import RateBy
from base.models.base import ModelAbstractBase


class Desc_RateBy(ModelAbstractBase):
    description = models.ForeignKey(Description, on_delete=models.CASCADE)
    rateBy = models.ManyToManyField(RateBy)

    def __str__(self):
        return f"description : {self.description.value}"

    class Meta:
        db_table = "desc_ratebys"
        verbose_name = "Desc_Rateby"
        verbose_name_plural = "Desc_Ratebys"

    
from django.db import models
from django.utils import timezone
from base.models.base import ModelAbstractBase


class RateBy(ModelAbstractBase):
    slug = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value

    class Meta:
        db_table = "ratebys"
        verbose_name = "Rateby"
        verbose_name_plural = "Ratebys"

from django.db import models
from django.utils import timezone
from base.models.base import ModelAbstractBase


class Description(ModelAbstractBase):
    slug = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "descriptions"
        verbose_name = "Description"
        verbose_name_plural = "Descriptions"

    @classmethod
    def get_description_obj(cls, **criteria):
        """
        Returns object
        """
        return cls.objects.get(**criteria)

    @classmethod
    def get_description_queryset(cls, **criteria):
        """
        Returns queryset
        """
        return cls.objects.filter(**criteria)

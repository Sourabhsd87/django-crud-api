from django.contrib import admin
from .models import Description, RateBy, Desc_RateBy

EXCLUDE_FIELDS = ["internal_id", "created_on", "updated_on"]


class BaseAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # return super().get_list_display(request)
        return [
            field.name
            for field in self.model._meta.fields
            if field.name not in EXCLUDE_FIELDS
        ]

    def get_search_fields(self, request):
        # return super().get_search_fields(request)
        return [field.name for field in self.model._meta.fields]

    def get_list_filter(self, request):
        # return super().get_list_filter(request)
        return [
            field.name
            for field in self.model._meta.fields
            if field.get_internal_type() in ["CharField", "BooleanField"]
        ]


# Register your models here.
admin.site.register(Description)
admin.site.register(RateBy)


@admin.register(Desc_RateBy)
class DescRateByAdmin(admin.ModelAdmin):
    list_display = ["description"]
    filter_horizontal = ["rateBy"]

from django.urls import path
from .views import (
    DescriptionCreateAPIView,
    DescriptionUpdateAPIView,
    DescriptionDeleteAPIView,
    RateByCreateAPIView,
    RateByUpdateAPIView,
    RateByDeleteAPIView,
    RateByListAPIView,
    DescRateByCreateAPIView,
    DescRateByUpdateAPIView,
    DescriptionListAPIView,
    ListRatebysByDescriptionAPIView,
    ListWarehouseActivityAPIView,
)

urlpatterns = [
    path("description/", DescriptionListAPIView.as_view(), name="description-list"),
    path(
        "description/create",
        DescriptionCreateAPIView.as_view(),
        name="description-create",
    ),
    path(
        "description/update/<uuid:pk>",
        DescriptionUpdateAPIView.as_view(),
        name="description-update",
    ),
    path(
        "description/delete/<uuid:pk>",
        DescriptionDeleteAPIView.as_view(),
        name="description-delete",
    ),
    path("rateby/", RateByListAPIView.as_view(), name="rateby-list"),
    path("rateby/create", RateByCreateAPIView.as_view(), name="rateBy-create"),
    path(
        "rateby/update/<uuid:pk>", RateByUpdateAPIView.as_view(), name="rateby-update"
    ),
    path(
        "rateby/delete/<uuid:pk>", RateByDeleteAPIView.as_view(), name="rateby-delete"
    ),
    path(
        "desc-rateby/create",
        DescRateByCreateAPIView.as_view(),
        name="desc-rateby-create",
    ),
    path(
        "desc-rateby/updateByDescription/<uuid:description_id>",
        DescRateByUpdateAPIView.as_view(),
        name="desc-rateby-create",
    ),
    path(
        "desc-rateby/getbydescription/<uuid:description_id>",
        ListRatebysByDescriptionAPIView.as_view(),
        name="get",
    ),
    path(
        "warehouse-activities/",
        ListWarehouseActivityAPIView.as_view(),
        name="list-warehouse-activity",
    ),
]

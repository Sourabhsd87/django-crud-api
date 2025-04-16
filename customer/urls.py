from django.urls import path
from customer.views.customer import (
    CustomerListAPIView,
    CustomerCreateAPIView,
    CustomerUpdateAPIView,
    CustomerDeleteAPIView,
)

urlpatterns = [
    path("customer/", CustomerListAPIView.as_view(), name="customer_list"),
    path("customer/create", CustomerCreateAPIView.as_view(), name="customer-create"),
    path(
        "customer/update/<uuid:internal_id>",
        CustomerUpdateAPIView.as_view(),
        name="update-customer",
    ),
    path(
        "customer/delete/<uuid:internal_id>",
        CustomerDeleteAPIView.as_view(),
        name="customer-delete",
    ),
]

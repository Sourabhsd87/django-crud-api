from rest_framework import serializers
from purchaseOrder.models.purchaseOrder import PurchaseOrder
class PurchaseOrderModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ["purchase_order","type","suffix","company","warehouse","carrier","services","pro_number"]

class PurchaseOrderListSerializer(serializers.Serializer):

    def get_purchaseOrder_data(**criteria):
        return PurchaseOrder.get_purchaseOrder_queryset(**criteria)

    def filter_purchaseOrder_data(self,data):

        request = self.context["request"]
        type_filter = request.GET.get("type")
        company_filter = request.GET.get("company")
        warehouse_filter = request.GET.get("warehouse")

        if type_filter:
            data = data.filter(type=type_filter)
        
        if company_filter:
            data = data.filter(company=company_filter)

        if warehouse_filter:
            data = data.filter(warehouse=warehouse_filter)

        return data
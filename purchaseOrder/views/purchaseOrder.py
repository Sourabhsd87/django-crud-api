from rest_framework.views import APIView
from purchaseOrder.serializers.purchase_order import PurchaseOrderListSerializer
class PurchaseOrderListAPIView(APIView):
        
    serializer_class = PurchaseOrderListSerializer

    def get(self,request):
        
        
        purchaseOrder_data = self.serializer_class.get_purchaseOrder_data()      
        
        
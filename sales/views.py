from rest_framework import viewsets, status
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSalesOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSalesOrAdmin]

    # FILTER + ROLE BASED DATA
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.all()

        if user.roles != 'admin':
            queryset = queryset.filter(created_by=user)

        status_param = self.request.query_params.get('status')
        customer = self.request.query_params.get('customer')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if customer:
            queryset = queryset.filter(customer_id=customer)

        return queryset.order_by('-created_at')



    def perform_create(self, serializer):
        serializer.save()

    # UPDATE STATUS (WITH STOCK RESTORE)
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['pending', 'completed', 'cancelled']:
            return Response({"error": "Invalid status"}, status=400)

        # STOCK RESTORE IF CANCELLED
        if new_status == 'cancelled' and order.status != 'cancelled':
            for item in order.items.all():
                product = item.product
                product.stock_quantity += item.quantity
                product.save()

        order.status = new_status
        order.save()

        return Response({"message": "Status updated successfully"})


    
    # SALES SUMMARY (ADVANCED)
    @action(detail=False, methods=['get'])
    def summary(self, request):
        orders = Order.objects.all()

        total_orders = orders.count()
        total_revenue = sum([order.total_price for order in orders])

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue
        })

    
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSalesOrAdmin


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()   # ✅ MUST ADD THIS LINE
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSalesOrAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Order.objects.all().order_by('-created_at')

        return Order.objects.filter(created_by=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()
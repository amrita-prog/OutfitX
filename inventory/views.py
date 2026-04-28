from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()

        name = self.request.query_params.get('name')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        low_stock = self.request.query_params.get('low_stock')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if low_stock == 'true':
            queryset = queryset.filter(stock_quantity__lt=10)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response({"error": "Quantity is required"}, status=400)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"error": "Invalid quantity"}, status=400)

        if product.stock_quantity + quantity < 0:
            return Response({"error": "Stock cannot be negative"}, status=400)

        product.stock_quantity += quantity
        product.save()

        return Response({
            "message": "Stock updated",
            "new_stock": product.stock_quantity
        })
    

    def get_permissions(self):
        user = self.request.user

        # ये actions सिर्फ admin + inventory कर सकते हैं
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'update_stock']:
            if user.roles not in ['admin', 'inventory']:
                raise PermissionDenied("Only admin or inventory can perform this action")

        return [permissions.IsAuthenticated()]
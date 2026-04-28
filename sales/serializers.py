from rest_framework import serializers
from .models import Order, OrderItem
from inventory.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        total_price = 0
        order = Order.objects.create(
            customer=validated_data['customer'],
            created_by=user,
            total_price=0
        )

        for item in items_data:
            product = Product.objects.get(id=item['product'].id)
            quantity = item['quantity']

            # STOCK CHECK
            if product.stock_quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}"
                )

            # PRICE CALCULATION
            price = product.price * quantity
            total_price += price

            # CREATE ORDER ITEM
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            # REDUCE STOCK
            product.stock_quantity -= quantity
            product.save()

        order.total_price = total_price
        order.save()

        return order
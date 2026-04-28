from rest_framework import serializers
from .models import Invoice, Transaction
from sales.models import Order


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class InvoiceSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


class CreateInvoiceSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def validate(self, data):
        order_id = data.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")

        # Only completed order allowed
        if order.status != 'completed':
            raise serializers.ValidationError("Invoice can only be created for completed orders")

        # Prevent duplicate invoice
        if hasattr(order, 'invoice'):
            raise serializers.ValidationError("Invoice already exists for this order")

        data['order'] = order
        return data

    def create(self, validated_data):
        order = validated_data['order']

        invoice = Invoice.objects.create(
            order=order,
            total_amount=order.total_price
        )

        return invoice
    

class PaymentSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=[
        'upi', 'card', 'cash'
    ])

    def validate(self, data):
        invoice_id = data.get('invoice_id')

        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise serializers.ValidationError("Invoice not found")

        # Already paid
        if invoice.status == 'paid':
            raise serializers.ValidationError("Invoice already paid")

        data['invoice'] = invoice
        return data

    def create(self, validated_data):
        invoice = validated_data['invoice']
        payment_method = validated_data['payment_method']

        # Create Transaction
        transaction = Transaction.objects.create(
            invoice=invoice,
            amount=invoice.total_amount,
            payment_method=payment_method,
            status='success'
        )

        # Update Invoice
        invoice.status = 'paid'
        invoice.save()

        return transaction
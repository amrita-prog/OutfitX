from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Invoice, Transaction
from .serializers import (
    InvoiceSerializer,
    TransactionSerializer,
    CreateInvoiceSerializer,
    PaymentSerializer
)



class CreateInvoiceView(APIView):

    def post(self, request):
        serializer = CreateInvoiceSerializer(data=request.data)

        if serializer.is_valid():
            invoice = serializer.save()

            return Response({
                "message": "Invoice created successfully",
                "data": InvoiceSerializer(invoice).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MakePaymentView(APIView):

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            transaction = serializer.save()

            return Response({
                "message": "Payment successful",
                "transaction": TransactionSerializer(transaction).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListView(APIView):

    def get(self, request):
        transactions = Transaction.objects.all()

        status_param = request.query_params.get('status')
        method_param = request.query_params.get('payment_method')

        if status_param:
            transactions = transactions.filter(status=status_param)

        if method_param:
            transactions = transactions.filter(payment_method=method_param)

        transactions = transactions.order_by('-created_at')

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

class InvoiceDetailView(APIView):

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=404)

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
    

class InvoiceListView(APIView):

    def get(self, request):
        invoices = Invoice.objects.all()

        status_param = request.query_params.get('status')

        if status_param:
            invoices = invoices.filter(status=status_param)

        invoices = invoices.order_by('-created_at')

        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)
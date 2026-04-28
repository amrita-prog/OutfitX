from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import CustomUser
from leads.models import Lead, Customer
from inventory.models import Product
from sales.models import Order
from invoices.models import Invoice

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    total_users = CustomUser.objects.count()

    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status='new').count()

    total_customers = Customer.objects.count()

    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock_quantity__lt=10).count()

    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='completed').count()
    pending_orders = Order.objects.filter(status='pending').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()

    total_revenue = sum(
        order.total_price for order in Order.objects.filter(status='completed')
    )

    total_invoices = Invoice.objects.count()
    paid_invoices = Invoice.objects.filter(status='paid').count()
    pending_invoices = Invoice.objects.filter(status='generated').count()

    return Response({
        "total_users": total_users,
        "total_leads": total_leads,
        "new_leads": new_leads,
        "total_customers": total_customers,
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "pending_orders": pending_orders,
        "cancelled_orders": cancelled_orders,
        "total_revenue": total_revenue,
        "total_invoices": total_invoices,
        "paid_invoices": paid_invoices,
        "pending_invoices": pending_invoices
    })
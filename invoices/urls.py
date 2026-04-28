from django.urls import path
from .views import (
    CreateInvoiceView,
    MakePaymentView,
    TransactionListView,
    InvoiceDetailView,
    InvoiceListView
)

urlpatterns = [
    path('create/', CreateInvoiceView.as_view()),
    path('pay/', MakePaymentView.as_view()),
    path('transactions/', TransactionListView.as_view()),
    path('<int:pk>/', InvoiceDetailView.as_view()),
    path('', InvoiceListView.as_view()),
]




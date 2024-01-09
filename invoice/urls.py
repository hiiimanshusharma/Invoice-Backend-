from django.urls import path, include
from .views import InvoiceView, InvoiceDetailView

urlpatterns = [
    path('view/', InvoiceView.as_view(), name='invoice-view'),
    path('create/', InvoiceView.as_view(), name='invoice-create'),
    path('edit/<int:id>/', InvoiceView.as_view(), name='invoice-edit'),
    path('delete/<int:id>/', InvoiceView.as_view(), name='invoice-delete'),
    path('detail/<int:id>/', InvoiceDetailView.as_view(), name='invoice-detail')
]
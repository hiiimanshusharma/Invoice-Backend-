from rest_framework import serializers

from .models import Invoice, InvoiceDetail


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ('id', 'customerName', 'date')

class InvoiceDetailSerializer(serializers.ModelSerializer):
    customerName = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceDetail
        fields = ('customerName','date', 'description', 'quantity', 'unit_price', 'price')

    def get_customerName(self, obj):
        return obj.invoice.customerName
    
    def get_date(self, obj):
        return obj.invoice.date
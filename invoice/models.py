from django.db import models

class Invoice(models.Model):
    date  = models.DateTimeField(auto_now_add=True)
    customerName = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"{self.customerName}-{self.id}"

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(max_length=10000, null=False, blank=False)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.invoice.customerName}-{self.id}"
    
    # def get_price()
    





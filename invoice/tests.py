from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Invoice, InvoiceDetail

class InvoiceViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_invoices(self):
        response = self.client.get(reverse('invoice-view'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assuming you have some invoices in the database, add them for testing
        Invoice.objects.create(customerName='Test Customer')
        response = self.client.get(reverse('invoice-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invoice(self):
        data = {
            'customerName': 'Test Customer',
            'description': 'Test Description',
            'quantity': 1,
            'unitPrice': 10.0,
            'price': 10.0
        }
        response = self.client.post(reverse('invoice-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_invoice(self):
        invoice = Invoice.objects.create(customerName='Test Customer')
        data = {
            'customerName': 'Updated Customer'
        }
        response = self.client.put(reverse('invoice-edit', args=[invoice.id]), data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

        if response.status_code == status.HTTP_200_OK:
            updated_invoice = Invoice.objects.get(id=invoice.id)
            self.assertEqual(updated_invoice.customerName, 'Updated Customer')

    def test_delete_invoice(self):
        invoice = Invoice.objects.create(customerName='Test Customer')
        response = self.client.delete(reverse('invoice-delete', args=[invoice.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Invoice.objects.filter(id=invoice.id).exists())

class InvoiceDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_invoice_detail(self):
        invoice = Invoice.objects.create(customerName='Test Customer')
        invoice_detail = InvoiceDetail.objects.create(
            invoice=invoice,
            description='Test Description',
            quantity=1,
            unit_price=10.0,
            price=10.0
        )
        response = self.client.get(reverse('invoice-detail', args=[invoice.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test Description')

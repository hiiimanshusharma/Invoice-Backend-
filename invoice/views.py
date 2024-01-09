from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer



class InvoiceView(APIView):
    
    def get(self, request):
        
        try:
            if not Invoice.objects.all().exists():
                return Response({'detail':'No Invoice found'}, status=status.HTTP_204_NO_CONTENT)
            invoice_objs = Invoice.objects.all()
            invoice_sez = InvoiceSerializer(invoice_objs, many=True)
            return Response(invoice_sez.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'detail':f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            data = request.data
            errors = {}
            customerName = data.get('customerName')
            description = data.get('description')
            quantity = data.get('quantity')
            unit_price = data.get('unitPrice')
            price = data.get('price')

            if not customerName:
                errors['customerName'] = 'Customer Name is required'
            if not description:
                errors['description'] = 'Description is required'
            
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            invoice = Invoice.objects.create(
                customerName = customerName
            )

            invoce_detail = InvoiceDetail.objects.create(
                invoice = invoice,
                description = description,
                quantity=quantity,
                unit_price=unit_price,
                price=price
            )

            return Response({'detail':'Invoice created Sucessfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'detail':f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        invoice_id = self.kwargs['id']
        try:
            data = request.data
            customerName = data.get('customerName')
            description = data.get('description')
            quantity = data.get('quantity')
            unit_price = data.get('unitPrice')
            price = data.get('price') 

            if not Invoice.objects.filter(id=invoice_id).exists():
                return Response({'detail':'Invoice doesnt exist'}, status=status.HTTP_204_NO_CONTENT)

            invoice_obj = Invoice.objects.get(id=invoice_id)
            Invoice.objects.filter(id=invoice_id).update(
                customerName=customerName
            )

            if not InvoiceDetail.objects.filter(invoice=invoice_obj).exists():
                return Response({'detail':'Invoice Detail doesnt exist'}, status=status.HTTP_204_NO_CONTENT)

            InvoiceDetail.objects.filter(invoice=invoice_obj).update(
                description=description,
                quantity=quantity,
                unit_price=unit_price,
                price=price
            )

            return Response({'detail':'Invoice edited successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        invoice_id = self.kwargs['id']
        try:
            if not Invoice.objects.filter(id=invoice_id).exists():
                return Response({'detail':'Invoice doesnt exists'}, status=status.HTTP_204_NO_CONTENT)
            invoice_obj = Invoice.objects.get(id=invoice_id)
            invoice_obj.delete()
            return Response({'detail':'Invoice deleted succesfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailView(APIView):
        
        def get(self, request, *args, **kwargs):
            invoice_id = self.kwargs['id']
            try:
                if not Invoice.objects.filter(id=invoice_id).exists():
                    return Response({'detail':'Invoice doesnt exists'}, status=status.HTTP_204_NO_CONTENT)
                invoice_obj = Invoice.objects.get(id=invoice_id)
                invoicedetail_obj = InvoiceDetail.objects.get(invoice=invoice_obj)
                invoice_sez = InvoiceDetailSerializer(invoicedetail_obj)

                return Response(invoice_sez.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail':f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    
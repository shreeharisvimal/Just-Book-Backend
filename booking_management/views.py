from io import BytesIO
from django.conf import settings
import razorpay
from django.http import HttpResponse
from show_management.models import Show
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated  
from rest_framework.generics import GenericAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os

from . import models
from . import serializers

# Create your views here.

class PaymentHandler(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        if user.is_anonymous:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        amount = data.get('amount_paid') 
        currency = 'INR'
        payment_data = {
            'amount': amount * 100,
            'currency': currency,
            'payment_capture': '1'
        }
        try:
            razorpay_order = client.order.create(data=payment_data)
            payment = models.Payment.objects.create(
                user=user,
                payment_status='PENDING',
                payment_id=razorpay_order['id'],
                amount_paid=amount
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data={
            'razorpay_payment_id': razorpay_order['id'],
            'payment': serializers.PaymentSerializer(payment).data
        }, status=status.HTTP_200_OK)
    
class BookingHandler(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers)
        data = request.data
        user = request.user
        if user.is_anonymous:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        payment = models.Payment.objects.get(user=user, payment_id=str(data.get('pay_id')))
        show = Show.objects.get(id=int(data.get('show_details')))
        try:
            booking = models.Booking.objects.create(
                user=user,
                payment_details=payment,
                no_of_seats=int(data.get('no_of_seats')),
                seats_name=str(data.get('seats_name')),
                show_details=show,
            )
            ticket = booking.Create_Unique_QR()
            print(ticket)
            payment.payment_status = 'SUCCESS'
            booking.booking_status = 'COMPLETED'
            payment.save()
            booking.save()
            
            return Response({"ticket":ticket.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FetchUserTickets(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, qr_code_id = None, id=None):
        user = request.user
        if id:
            try:
                print('ticket')
                ticket = models.Ticket.objects.get(id=id)
                data = ticket.get_ticket_data()
                # serializer = serializers.TicketSerializer(ticket)
                return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

        try:
            ticket = models.Ticket.objects.filter(user=user)
            if qr_code_id:
                qrcode = models.QRCode.objects.get(qr_code_id=qr_code_id)
                if qrcode.used == True:
                    ticket = ticket.filter(qr_code=qrcode.id)
                    data = serializers.TicketSerializer(ticket, many=True).data
                    return Response(data, status=status.HTTP_226_IM_USED)
                ticket = models.Ticket.objects.filter(qr_code=qrcode.id)
                print("THe tickets", ticket)
            data = serializers.TicketSerializer(ticket, many=True).data
            for ticket in data:
                if 'qr_code' in ticket and 'qr_code_image' in ticket['qr_code']:
                    ticket['qr_code']['qr_code_image'] = request.build_absolute_uri('/')[:-1] + ticket['qr_code']['qr_code_image']
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, qr_code_id):
        try:
            Qrcode = models.QRCode.objects.get(qr_code_id=qr_code_id)
            Qrcode.used = True
            Qrcode.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def generate_ticket_pdf(ticket_data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    y_position = 500

    qr_code_path = os.path.join(settings.MEDIA_ROOT, ticket_data['QR_code'].lstrip('/media/'))
    if os.path.exists(qr_code_path):
        c.drawImage(qr_code_path, 250, y_position, width=100, height=100)
        y_position -= 120

    for key, value in ticket_data.items():
        if key != 'QR_code':
            c.drawString(100, y_position, f"{key}: {value}")
            y_position -= 20

    c.showPage()
    c.save()
    return buffer.getvalue()

class DownloadTicketPdf(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            ticket = models.Ticket.objects.get(user=request.user, pk=int(id))
            ticket_data = ticket.get_ticket_data()
            pdf_content = generate_ticket_pdf(ticket_data)
            filename = f"ticket_{ticket.id}.pdf"
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return HttpResponse(f"Ticket not found {e}", status=404)
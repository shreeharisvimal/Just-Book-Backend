from rest_framework import serializers
from . import models



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = '__all__'
        depth = 2
        
class QrSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QRCode
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    booking = BookingSerializer()
    qr_code = QrSerializer()

    class Meta:
        model = models.Ticket
        fields = '__all__'
        depth = 2
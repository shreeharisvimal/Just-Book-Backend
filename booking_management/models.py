import uuid
from django.db import models
from django.conf import settings
from user_management import models as UserModel
from show_management import models as ShowModel
from .utils import Get_Qr_Code

class QRCode(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='qr_code')
    qr_code_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_code_image = models.ImageField(upload_to='qrcodes/', blank=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.qr_code_image:
            qr_data = f"{settings.CORS_ALLOWED_ORIGINS[0]}/verify/{self.qr_code_id}/"
            self.qr_code_image = Get_Qr_Code(qr_data)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class Ticket(models.Model):
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE)
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='ticket')
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('booking', 'qr_code')
        ordering = ['-id']

    def get_ticket_data(self):
        return {
            'QR_code': self.qr_code.qr_code_image.url, 
            'Movie': self.booking.show_details.movie.title,
            'Seats': self.booking.seats_name,
            'Theater': self.booking.show_details.theater.theater_name,
            'Screen': self.booking.show_details.screen.name,
            'Date': self.booking.show_details.show_date,
            'Time': self.booking.show_details.show_time,
        }



class Payment(models.Model):
    PAYMENT_STATUS = (
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
    )
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20, default='PENDING')
    payment_id = models.TextField(default=uuid.uuid4)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    payment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_time']

class Booking(models.Model):
    BOOKING_STATUS = (
        ("PROCESSING", "Order Processing"),
        ("FAILED", "booking Failed"),
        ("COMPLETE", "Booking Complete"),
        ("CANCELLED", "Booking Cancelled"),
    )

    user = models.ForeignKey(UserModel.User, on_delete=models.SET_NULL, null=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True, editable=False)
    payment_details = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    booking_status = models.CharField(choices=BOOKING_STATUS, max_length=20, default='PROCESSING')
    no_of_seats = models.IntegerField(default=1)
    seats_name = models.TextField()
    show_details = models.ForeignKey(ShowModel.Show, on_delete=models.CASCADE)
    ordered_time = models.DateTimeField(auto_now_add=True)
    booking_updated_time = models.DateTimeField(auto_now=True)
    cancel_reason = models.TextField(max_length=200, null=True, blank=True)

    
    class Meta:
        ordering = ['-ordered_time']

    def Create_Unique_QR(self):
        qr = QRCode.objects.create(booking=self)
        ticket = Ticket.objects.create(user= self.user, booking=self, qr_code=qr)
        return ticket

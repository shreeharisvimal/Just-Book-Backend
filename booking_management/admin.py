from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Booking)
admin.site.register(models.Ticket)
admin.site.register(models.QRCode)


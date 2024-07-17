from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Screen)
admin.site.register(models.ScreenType)
admin.site.register(models.Seat_type)
admin.site.register(models.Theater)
admin.site.register(models.Seats)


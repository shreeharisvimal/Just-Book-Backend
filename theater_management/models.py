from django.db import models
from movie_management.models import Movie

class Theater(models.Model):

    THEATER_STATUS = (
            ("APPROVED", "Theater Was Approved"),
            ("PENDING", "Theater is Pending for Approval"),
            ("REJECTED", "Theater is Rejected by JustBook"),
        )  

    theater_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=120)
    address = models.TextField(default=' ', null=True, blank=True)
    city = models.TextField(default=' ', null=True, blank=True)
    state = models.TextField(default=' ', null=True, blank=True)
    description = models.TextField()
    theater_status = models.CharField(max_length=10, choices=THEATER_STATUS, default='PENDING')
    no_of_screens = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.theater_name
    
    

class ScreenType(models.Model):
    name = models.CharField(max_length=255)
    price_multi = models.CharField(max_length=50)



class Screen(models.Model):
    name = models.CharField(max_length=255)
    total_seats = models.IntegerField()
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='screens')
    screen_type = models.ForeignKey(ScreenType, on_delete=models.CASCADE, related_name='screens')

    def __str__(self):
        return f'{self.name} - {self.screen_type.name}'
    
    def clean(self):
        super().clean()
        if self.theater.no_of_screens is None:
            self.theater.no_of_screens = 1
        else:
            self.theater.no_of_screens += 1
        self.theater.save()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Seat_type(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.SET_NULL, related_name='theater')
    name = models.CharField(max_length=255)
    price_multi = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.name} - {self.name} - {self.price_multi}'

class Seats(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.SET_NULL, related_name='seats')
    seat_allocation = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f'{self.seat_allocation} - screen {self.screen} - {self.screen.theater.theater_name}'
    
from django.db import models
from django.apps import apps

class CustomeQueryset(models.QuerySet):
    def active(self):
        return self.filter(is_over=False)
    
class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomeQueryset(self.model, using=self._db).active()
    
class Show(models.Model):
    movie = models.ForeignKey('movie_management.Movie', on_delete=models.CASCADE)
    theater = models.ForeignKey('theater_management.Theater', on_delete=models.CASCADE, blank=True, null=True)
    screen = models.ForeignKey('theater_management.Screen', on_delete=models.CASCADE, blank=True, null=True)
    seatAllocation = models.JSONField(default=dict)
    show_date = models.DateField()
    show_time = models.TimeField()
    price = models.IntegerField()
    is_over = models.BooleanField(default=False)

    objects = CustomManager()

    def __str__(self):
        return f"{self.movie} -{self.theater} - {self.screen} - {self.show_date} - {self.show_time} "
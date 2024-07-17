from django.db import models
from theater_management import models as Theatermodels
from movie_management import models as moviemodels


class CustomeQueryset(models.QuerySet):
    def active(self):
        return self.filter(is_over=False)
    
class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomeQueryset(self.model, using=self._db).active()
    

class Show(models.Model):
    movie = models.ForeignKey(moviemodels.Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theatermodels.Theater, on_delete=models.CASCADE, blank=True, null=True)
    screen = models.ForeignKey(Theatermodels.Screen, on_delete=models.CASCADE, blank=True, null=True)
    seatAllocation = models.JSONField(default=dict)
    show_date = models.DateField()
    show_time = models.TimeField()
    price = models.IntegerField()
    is_over = models.BooleanField(default=False)

    objects = CustomManager()

    def __str__(self):
        return f"{self.movie} -{self.theater} - {self.screen} - {self.show_date} - {self.show_time} "



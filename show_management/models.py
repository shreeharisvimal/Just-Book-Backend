from django.db import models
from django.apps import apps
from datetime import date

class CustomeQueryset(models.QuerySet):
    def active(self):
        return self.filter(is_over=False)
    
class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomeQueryset(self.model, using=self._db).active()

    def filter(self, *args, **kwargs):
        qs = super().filter(*args, **kwargs)
        return qs.filter(show_date__gte=date.today())

    def get(self, *args, **kwargs):
        try:
            instance = super().get(*args, **kwargs)
            if instance.show_date < date.today():
                raise ValueError("The show date is in the past.")
            return instance
        except self.model.DoesNotExist:
            raise ValueError("Show not found or is not active.")
        except Exception as e:
            raise e
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
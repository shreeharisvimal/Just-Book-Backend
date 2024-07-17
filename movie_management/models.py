from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    title = models.CharField(max_length=100)
    tmdb_id = models.IntegerField()
    poster_path = models.CharField(max_length=225)
    background_path = models.CharField(max_length=225)
    video_key = models.CharField(max_length=225)
    release_date = models.CharField(max_length=255, default='00/00/0000')
    language = models.CharField(max_length=255, default=' ')
    # genre = models.JSONField()

    def __str__(self):
        return self.title


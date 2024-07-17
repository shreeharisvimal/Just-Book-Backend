from rest_framework import serializers
from . import models


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ['id', 'name']
        

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = '__all__'


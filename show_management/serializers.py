from rest_framework import serializers
from . import models
from theater_management.models import Theater, Screen, Seats
from movie_management.models import Movie
from rest_framework.response import Response
from rest_framework import permissions, status



class showSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    theater = serializers.PrimaryKeyRelatedField(queryset=Theater.objects.filter(theater_status='APPROVED'))
    screen = serializers.PrimaryKeyRelatedField(queryset=Screen.objects.all())

    class Meta:
        model = models.Show
        fields = '__all__'
    
    def create(self, validated_data):
        screenId = validated_data.pop('screen')
        try:
            seat = Seats.objects.get(screen=screenId)
        except Seats.DoesNotExist:
            raise serializers.ValidationError("Create Error: Seats not found for the screen.")

        if models.Show.objects.filter(screen=screenId, seatAllocation=seat.seat_allocation, show_date=validated_data['show_date'], show_time=validated_data['show_time']).exists():
            raise serializers.ValidationError("Show already exists for the given screen, date, and time.")
        return models.Show.objects.create(screen=screenId, seatAllocation=seat.seat_allocation, **validated_data)
        
class showFetchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Show
        fields = '__all__'
        depth = 2

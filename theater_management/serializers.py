from rest_framework import serializers
from . import models


from rest_framework import permissions, status
from rest_framework.response import Response

    


class TheaterSerializer(serializers.ModelSerializer):
    screen = serializers.SerializerMethodField()

    class Meta:
        model = models.Theater
        fields = '__all__'
    
    def get_screen(self, obj):
        screen = models.Screen.objects.filter(theater=obj)
        return ScreenSerializer(screen, many=True).data



class ScreenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ScreenType
        fields = ['id','name','price_multi']


class ScreenSerializer(serializers.ModelSerializer):
    theater = serializers.PrimaryKeyRelatedField(queryset=models.Theater.objects.all())
    screen_type = serializers.PrimaryKeyRelatedField(queryset=models.ScreenType.objects.all())
    class Meta:
        model = models.Screen
        fields = ['id', 'name', 'total_seats', 'theater', 'screen_type']

    def create(self, validated_data):
        theater = validated_data.pop('theater')
        screen_type = validated_data.pop('screen_type')
        
        screen = models.Screen.objects.create(theater=theater, screen_type=screen_type, **validated_data)
        # screen.UpdateOnOfTheaterScreen()
        return screen

class SeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seats
        fields = '__all__'
    
class ScreenGetSerializer(serializers.ModelSerializer):
    seats = SeatsSerializer(many=True, read_only=True)
    class Meta:
        model = models.Screen
        fields = '__all__'
        depth = 1

class SeatTypeCreateSerializer(serializers.ModelSerializer):
    theater  = serializers.PrimaryKeyRelatedField(queryset = models.Theater.objects.all())

    class Meta:
        model = models.Seat_type
        fields = '__all__'

class SeatTypeGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Seat_type
        fields = '__all__'
        depth=1



class SeatAllocationCreateSerializer(serializers.ModelSerializer):
    screen = serializers.PrimaryKeyRelatedField(queryset=models.Screen.objects.all())

    class Meta:
        model = models.Seats
        fields = '__all__'

    def create(self, validated_data):
        screen = validated_data.pop('screen')
        seats = models.Seats.objects.create(screen=screen, **validated_data)
        return seats

    def get_screen(self, obj):
        return ScreenSerializer(obj.screen).data
        
class SeatAllocationGetOrDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seats
        fields = '__all__'
        depth = 2
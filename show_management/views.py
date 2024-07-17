from django.shortcuts import render
from . import models
from . import serializers
from theater_management.models import Theater, Screen

from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView




class showCreateApi(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.showSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_226_IM_USED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, email):
        try:
            theaters = Theater.objects.filter(email=email)
            print(f"The theaters: {theaters}")
        except Theater.DoesNotExist:
            print('Error while fetching theater')
            return Response(status=status.HTTP_204_NO_CONTENT)

        shows = []
        for theater in theaters:
            theater_shows = models.Show.objects.filter(theater=theater.id)
            shows.extend(theater_shows)

        serializer = serializers.showFetchSerializer(shows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            show = models.Show.objects.get(id=id)
            show.delete()
            return Response(status=status.HTTP_200_OK)
        except models.Show.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    



class ShowFetchWIthMovie(GenericAPIView):
    def get(self, request, id):
        try:
            shows = models.Show.objects.filter(movie__in = [id])
            serializer = serializers.showFetchSerializer(shows, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response(status=status.HTTP_302_FOUND)
        
class ShowFetchWIthid(GenericAPIView):
    def get(self, request, id):
        try:
            shows = models.Show.objects.filter(id=id, is_over=False)
            serializer = serializers.showFetchSerializer(shows, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response(status=status.HTTP_302_FOUND)
        
class ShowFetchAll(ListCreateAPIView):
    queryset = models.Show.objects.filter(is_over=False)
    serializer_class = serializers.showFetchSerializer

class UpdateShowSeats(GenericAPIView):

    def put(self, request, id):
        show = models.Show.objects.get(id=id)
        show.seatAllocation = request.data['seatAllocation']
        show.save()
        return Response(status=status.HTTP_200_OK)

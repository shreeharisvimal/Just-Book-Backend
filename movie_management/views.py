from . import models
from django.http import HttpResponse
from . import models
from . import serializers

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny


class GenreListCreateAPIView(ListCreateAPIView):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer

class GenreRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field='id'

class LanguageListCreateAPIView(ListCreateAPIView):
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer

class LanguageRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    lookup_field = 'id'

class MovieListCreateAPIView(ListCreateAPIView):
    queryset = models.Movie.objects.all()
    serializer_class =  serializers.MovieSerializer
    permission_classes =[AllowAny]

class movieListFetchAPIView(APIView):
    def get(self, request, id):
        movies = models.Movie.objects.filter(id=id)
        serializer =  serializers.MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = models.Movie.objects.all()
    serializer_class =  serializers.MovieSerializer
    lookup_field='id'
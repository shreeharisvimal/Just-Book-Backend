from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('genres/', views.GenreListCreateAPIView.as_view(), name='genres-list-create'),
    path('genres/<int:id>/', views.GenreRetrieveDestroyAPIView.as_view(), name='genre-retrieve-destroy'),
    path('language/',views.LanguageListCreateAPIView.as_view(), name='language-list-create' ),
    path('language/<int:id>/',views.LanguageRetrieveDestroyAPIView.as_view(), name='language-retieve-destroy' ),
    path('movieListCreateAPIView/',views.MovieListCreateAPIView.as_view(), name='managementcreate'),
    path('movieListFetchAPIView/<int:id>/',views.movieListFetchAPIView.as_view(), name='movieListFetchAPIView'),
    path('movieRetrieveDestroyAPIView/<int:id>/',views.MovieRetrieveDestroyAPIView.as_view(), name='managementdelete'),
]

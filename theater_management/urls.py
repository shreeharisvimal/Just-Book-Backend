from . import views
from django.urls import path




urlpatterns = [
    path('TheaterApiListCreateAPIView/', views.TheaterApiListCreateAPIView.as_view(), name='TheaterApiListCreateAPIView'),    
    path('TheaterPutClassApi/<int:id>/', views.TheaterPutClassApi.as_view(), name='TheaterPutClassApi'),    
    path('FetchTheaterStaff/<str:email>/', views.FetchTheaterStaff.as_view(), name='FetchTheaterStaff'),    
    path('TheaterApiRetrieveUpdateDestroyAPIView/<int:id>/', views.TheaterApiRetrieveUpdateDestroyAPIView.as_view(), name='TheaterApiRetrieveUpdateDestroyAPIView'),
   
    path('ScreenTypeApiCreate/', views.ScreenTypePostGet.as_view(), name='ScreenTypeCreate'),
    path('ScreenTypeApiDelete/<int:id>/', views.ScreenTypeDeletePut.as_view(), name='ScreenTypeRetrive'),
    
    path('ScreenApiCreate/', views.ScreenPostGet.as_view(), name='ScreenCreate'),
    path('ScreenApiGet/<str:email>/', views.ScreenGet.as_view(), name='ScreenCreate'),
    path('ScreenApiDelete/<int:id>/', views.ScreenDeletePut.as_view(), name='ScreenRetrive'),
    path('ScreenApiGetShow/<int:id>/', views.ScreenApiGetShow.as_view(), name='showCreateApiGet'),

    path("SeatTypeCreateApi/", views.SeatTypeCreateAPI.as_view(), name='SeatTypeCreateApi'),
    path('SeatTypeFetch/', views.SeatTypeFetchAPI.as_view(), name='SeatTypeFetch'),
    path("SeatTypeDeleteApi/<int:id>/", views.SeatTypeDeleteApi.as_view(), name='SeatTypeDeleteApi'),

    path('SeatAllocationCreateApi/', views.SeatAllocationCreateApi.as_view(), name='SeatAllocationCreateApi'),
    path('SeatAllocationCreateApi/<int:id>/', views.SeatAllocationCreateApi.as_view(), name='SeatAllocationCreateApi'),

    path('SeatAllocationApiDelete/<int:id>/', views.SeatAllocationApiDelete.as_view(), name='SeatAllocationApiDelete'),

    
 ]
 
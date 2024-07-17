from django.urls import path
from . import views


urlpatterns = [
    path('showCreateApi/', views.showCreateApi.as_view(), name='showCreateApi'),
    path('showCreateApi/email/<str:email>/', views.showCreateApi.as_view(), name='showCreateApiByEmail'),
    path('showCreateApi/id/<int:id>/', views.showCreateApi.as_view(), name='showCreateApiById'),
    path('ShowFetchWIthMovie/<int:id>/', views.ShowFetchWIthMovie.as_view(), name='ShowFetchWIthMovie'),
    path('ShowFetchWIthid/<int:id>/', views.ShowFetchWIthid.as_view(), name='ShowFetchWIthid'),
    path('ShowFetchAll/', views.ShowFetchAll.as_view(), name='ShowFetchAll'),

    path('UpdateShowSeats/<int:id>/', views.UpdateShowSeats.as_view(), name='UpdateShowSeats'),
    
]

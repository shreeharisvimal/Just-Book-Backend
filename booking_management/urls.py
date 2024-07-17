from django.urls import path
from . import views


urlpatterns = [
    # path('verify/', views.)
    path('RazorPay/', views.PaymentHandler.as_view(), name='PaymentHandler'),
    path('BookingHandler/', views.BookingHandler.as_view(), name='BookingHandler'),

    path('FetchTickets/', views.FetchUserTickets.as_view(), name='FetchTickets'),
    path('FetchTickets/<int:id>/', views.FetchUserTickets.as_view(), name='FetchTickets'),
    path('FetchTickets/verify/<str:qr_code_id>/', views.FetchUserTickets.as_view(), name='FetchTickets'),

    path('download/pdf/<int:id>/', views.DownloadTicketPdf.as_view(), name='DownloadPdf'),

]

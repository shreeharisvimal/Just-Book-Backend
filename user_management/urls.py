from django.urls import path
from . import views

urlpatterns = [
    path('SignInOrUp/', views.Userauths.as_view(), name='UserAuth'),
    path('googleAuth/', views.googleAuth.as_view(), name='googleAuth'),
    path('PasswordManagement/', views.PasswordManagement.as_view(), name='pass'),
    path('logout/', views.LogoutView.as_view(), name='LogOut'),
    path('getLoginOtp/<str:auth>/', views.OtpgetView.as_view(), name='OtpGet'),
    path('AdminAuth/', views.AdminAuth.as_view(), name="Admin_login"),
    path('StaffAuth/', views.StaffAuth.as_view(), name="Staff_Auth"),
    path('StaffDelete/<int:id>/', views.StaffDelete.as_view(), name="StaffDelete"),
    path('', views.UserProfilePage.as_view(), name='Userpage'),


    path('Profile/', views.UserProfilePage.as_view(), name='Profile' ),

]

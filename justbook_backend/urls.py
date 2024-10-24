from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings
from user_management.views import MyRefreshTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/',MyRefreshTokenObtainPairView.as_view(),name ='token_refresh'),
    
    path('',include('user_management.urls')),
    path('movie/', include('movie_management.urls')),
    path('theater/', include('theater_management.urls')),
    path('show/', include('show_management.urls')),
    path('booking/', include('booking_management.urls')),

    

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
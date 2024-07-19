from venv import logger

from django.conf import settings
from . import models
from django.http import HttpResponse
from . import models
from random import randint

import logging

from . import serializers
from django.views import View
from django.db.models import Q

from user_management.task import send_otp_to_email, send_otp_to_phone

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer





class MyRefreshTokenObtainPairSerializer(TokenRefreshSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

class MyRefreshTokenObtainPairView(TokenRefreshView):

    serializer_class = MyRefreshTokenObtainPairSerializer



class googleAuth(View):
    # def post(self, request):
    #     token = request.POST.get('token')
    pass



class Userauths(APIView):

    def post(self, request):
        data = request.data
        email = data.get('email', None)
        phone = data.get('phone', None)
        if email:
            user = models.User.objects.filter(email=email).first()
        else:
            user = models.User.objects.filter(phone=phone).first()
        
        if user is None:
            serializer = serializers.UserCreateEmailSerializer(data=data)
            if serializer.is_valid():
                new_user = serializer.create_user(serializer.validated_data)
                user_serializer = serializers.LoginSerializer(new_user, context={'request': request})
                val = user_serializer.validate(attrs={'email':email, 'phone':phone})
                return Response({
                    'userdata': val,
                    'message': "Thank you for signing up to JustBook"
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'The user details are not valid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logserializer = serializers.LoginSerializer(user, data=request.data, context={'request': request})
            if logserializer.is_valid():
                val = logserializer.validate(attrs={'email':email, 'phone':phone})
                return Response({
                    'userdata': val,
                    'message': "You have been logged in to JustBook"
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Please provide valid details'}, status=status.HTTP_400_BAD_REQUEST)
    

    
    def get(self, request):
        user = models.User.objects.all()
        serializer = serializers.UserGetSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OtpgetView(APIView):

    def get(self, request, auth):
        # print(auth)
        val = randint(111111, 999999)
        data = {}

        if '@gmail.com' in auth or '.com' in auth:
            data = {
                'otp': val,
                'email': auth
            }

            serializer = serializers.OtpSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                result = send_otp_to_email.delay(email, otp)
                return Response({'otp': val, 'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            data = {
                'otp': val,
                'phone': auth
            }
            serializer = serializers.PhoneOtpSerializer(data=data)
            if serializer.is_valid():
                phone = serializer.data['phone']
                otp = serializer.data['otp']
                send_otp_to_phone(phone, otp)
                return Response({'otp': val, 'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class AdminAuth(APIView):
    def post(self, request):
        serializer = serializers.AdminLoginSerializer(data = request.data ,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StaffAuth(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        staff = models.User.objects.filter(Q(is_staff=True) & Q(is_superuser=False))
        serializer = serializers.StaffSerializer(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class StaffDelete(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.User
    serializer_class = serializers.StaffSerializer
    lookup_field = 'id'

    
class UserProfilePage(GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        user_profile, created =  models.UserProfile.objects.get_or_create(user=request.user)
        serializer = serializers.UserProfileUpdateSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            user_profile.user.first_name = request.data['first_name']
            user_profile.user.last_name = request.data['last_name']
            user_profile.user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:
            user = models.User.objects.get(id=request.user.id)
            data = serializers.UserProfileSerializer(user).data
            try:
                profile = user.Profile
                profile_pic_url = settings.PRODUCTION_URL+profile.profile_pic.url if settings.PRODUCTION_URL else request.build_absolute_uri('/')[:-1] + profile.profile_pic.url 
                data['profile_pic'] = profile_pic_url
            except models.UserProfile.DoesNotExist:
                data['profile_pic'] = None  
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
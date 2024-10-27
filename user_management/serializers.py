from django.core.mail import send_mail
import requests
from rest_framework import serializers

from . import models
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import permissions, status


class UserCreateEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def check_user(self, validated_data):
        email = validated_data.get('email', None)
        phone = validated_data.get('phone', None)
        if models.User.objects.filter(email=email).exists():
            return True
        if models.User.objects.filter(phone=phone).exists():
            return True
        return False

    def create_user(self, validated_data):
        if not (validated_data.get('email') or validated_data.get('phone')):
            raise serializers.ValidationError('A phone number or email address is required.')
        try:
            if validated_data.get('email'):
                user = models.User.objects.create_user(email=validated_data.get('email'))
            else:
                user = models.User.objects.create_user(phone=validated_data.get('phone'))
            return user 
        except Exception as e:
            raise serializers.ValidationError(f'User could not be created: {e}')
    
class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'phone', 'first_name', 'last_name']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(max_length=40, required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(max_length=30, read_only=True)
    access_token = serializers.CharField(max_length=500, read_only=True)
    refresh_token = serializers.CharField(max_length=500, read_only=True)
    isAdmin = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.User
        fields = ['email', 'phone', 'first_name', 'access_token', 'refresh_token', 'isAdmin']

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')

        if email is not None or (len(email) > 3 if email else None):
            user = models.User.objects.filter(email=email).first()
        elif phone is not None or len(phone) > 5:
            user = models.User.objects.filter(phone=phone).first()
        else:
            raise serializers.ValidationError('Either email or phone is required.')

        if user is None:
            raise serializers.ValidationError('User not found.')

        token = user.tokens()
        return {
            'user_cred': user.email if user.email else user.phone,
            'isAdmin': user.is_superuser,
            'first_name': user.first_name,
            'user_id':user.pk,
            'access_token': token['AccessToken'],
            'refresh_token': token['RefreshToken'],
        }

class OtpSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = models.User
        fields = ['email', 'otp']


class PhoneOtpSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6, required=True)
    phone = serializers.CharField(max_length=35, required=True)

    class Meta:
        model = models.User
        fields = ['phone', 'otp']


class AdminLoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=50, write_only = True)
    password = serializers.CharField(max_length=50, write_only=True)
    access_token= serializers.CharField(max_length=500, read_only=True)
    refresh_token= serializers.CharField(max_length=500, read_only=True)
    isAdmin = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(max_length=30, read_only=True)

    class Meta:
        model = models.User
        fields = ['email','password','access_token','refresh_token','isAdmin', 'is_staff', 'first_name']

    def validate(self,attrs):
        email= attrs.get('email')
        password= attrs.get('password')
        user = None
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                token=user.tokens()
                return {
                    'user_cred': user.email if user.email else user.phone,
                    'isAdmin': user.is_superuser,
                    'is_staff':user.is_staff,
                    'first_name': user.first_name,
                    'access_token': token['AccessToken'],
                    'refresh_token': token['RefreshToken'],
                }
            return Response(data={'messages:invalid credential try again'})
        except models.User.DoesNotExist:
            if not user:
                return Response(data={'messages:user does not exits'})
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['password']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.UserProfile
        fields = ['profile_pic']

    

       

class StaffSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=50, write_only=True)
    phone= serializers.CharField(max_length=50)
    email= serializers.EmailField(max_length=50)
    access_token= serializers.CharField(max_length=500, read_only=True)
    refresh_token= serializers.CharField(max_length=500, read_only=True)
    isAdmin = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only = True)

    class Meta:
        model = models.User
        fields = ['id','first_name', 'last_name', 'password', 'phone', 'email', 'access_token','refresh_token','is_staff', 'isAdmin']
    
    def create(self, validated_data):
        if not models.User.objects.filter(email = validated_data['email'], ).exists():
            user = models.User.objects.create_staff(**validated_data)
            tokens = user.tokens()
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'email': user.email,
                'access_token': tokens['AccessToken'],
                'refresh_token': tokens['RefreshToken'],
                'is_staff': user.is_staff,
                'isAdmin': user.is_superuser
            }
        else:
                return Response({'message':f'Staff details is already in use'
                }, status=status.HTTP_409_CONFLICT)
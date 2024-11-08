from django.db import models
from random import randint
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

def RandNumber():
    return f'Unknown{randint(100000, 999999)}'

class Manager(BaseUserManager):
    def create_user(self, email=None, password=None, phone=None, first_name=None, last_name=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        if not (email or phone):
            raise ValueError('A phone number or email address is required.')
        user = self.model(email=email, phone=phone, first_name=first_name, last_name=last_name, **extra_fields)

        if not first_name:
            user.first_name = RandNumber()
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, phone=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if password is None:
            raise ValueError('Superuser must have a password')

        return self.create_user(email, password, phone, first_name, last_name, **extra_fields)

    def create_staff(self, email, password=None, phone=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)

        if password is None:
            raise ValueError('Staff must have a password')

        return self.create_user(email, password, phone, first_name, last_name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    objects = Manager()
    class Meta:
        ordering = ['-id']
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        refresh["first_name"] = str(self.first_name)
        refresh['user_cred'] = str(self.email) if self.email is not None else str(self.phone)
        refresh['user_id'] = str(self.id)
        refresh['isAdmin'] = str(self.is_superuser)
        refresh['is_Staff'] = str(self.is_staff)

        return {
            'RefreshToken': str(refresh),
            'AccessToken': str(refresh.access_token)
        }

    def __str__(self):
        return str(self.email) if self.email else str(self.phone)
    
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="Profile")
    profile_pic = models.ImageField(upload_to='profile',null=True,blank=True)
    
    def __str__(self):
        return str(self.user.first_name)
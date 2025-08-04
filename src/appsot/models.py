"""#login 
from django.db import models
from django.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class UserAccountManager(BaseUserManager):#helps us ceate usere
    def create_user(self,email,name,password = None)

    if not email:#if or not email is provided 
        raise ValueError('users must have an email adress')

    email = self.normalize_email(email)#naormalizing email to lowercase
    user = self.model(email = email, name = name)#passing in normalized email

    user.set_password(password)#set password function hashes the password automatically
    user.save()# save user
    return user

class UserAccount(AbstractBaseUser,PermissionsMixin):
    email= models.EmailField(max_length= 255,unique=True)#to use for logging in
    name  = modes.charField(max_length = 255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    ojects = UserAccountManager

    USERNAME_FIELD ='email'#default login
    #other creadentials 
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name

    def get__self__ (self):
        return self.email"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
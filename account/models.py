from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from helper.models import BaseModel
from django.core.validators import RegexValidator


class MyAccountManager(BaseUserManager):

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("User must enter phone number")
        phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, phone, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(phone, password, **extra_fields)

class UserData(AbstractUser, BaseModel):

    email = models.EmailField(verbose_name='email', max_length=60)
    phone_regex = RegexValidator(regex=r'(0/91)?[7-9][0-9]{9}',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    phone = models.CharField('phone number', validators=[phone_regex], max_length=17, unique=True )
    username = None
    name = models.CharField(max_length=50)
    image = models.ImageField(default='profile_pics/profile.png',  
                                     upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=100, null=True, blank=True)
    followers = models.ManyToManyField('UserData', related_name='followers_obj')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()

    def __str__(self):
        return self.name


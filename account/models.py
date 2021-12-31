from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.text import slugify


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'post/{author_id}/{title}-{filename}'.format(author_id=str(instance.author.id), title=str(instance.title), filename=filename)
    return file_path


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


class UserData(AbstractUser):

    email = models.EmailField(verbose_name='email', max_length=60)
    phone_regex = RegexValidator(regex=r'(0/91)?[7-9][0-9]{9}',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    phone = models.CharField('phone number', validators=[phone_regex], max_length=17, unique=True )
    username = None
    name = models.CharField(max_length=50)
    friends = models.ManyToManyField('UserData', blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()

    def __str__(self):
        return self.name


class PostData(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=300, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    author = models.ForeignKey(UserData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    upload_at = models.DateTimeField(auto_now=True)
    user_like = models.ManyToManyField(UserData, related_name='images_liked', blank=True )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.created_at.year, self.created_at.month, self.created_at.day, self.slug])

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.title), slugify(self.author)))
        super(PostData, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-upload_at',]

class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserData, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserData, related_name="to_user", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user}-->{self.to_user}"





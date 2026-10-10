from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_integer, validate_email
from .validators import validate_phone_ir
import uuid
from django.conf import settings
from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        db_index=True,
        editable=False
    )
    phone = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[validate_integer, validate_phone_ir], 
        db_index=True,
    ) 
    email = models.EmailField(
        max_length=80, 
        unique=True, 
        null=True, 
        blank=True, 
        validators=[validate_email]
    )

    last_name = None
    first_name = None

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email", "username"]

    objects = UserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile")
    profile = models.ImageField(upload_to="profiles/", default="templates/accounts/default_img_profile/User-16.png")
    bio = models.TextField(max_length=200, null=True, blank=True)
    username_id = models.CharField(max_length=60, unique=True, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    # jalali date
    date_of_birth = models.DateTimeField(null=True, blank=True)


    
from django.db import models

# Create your models here.
# infrastructure/models.py
from django.conf import settings
import uuid

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    dni = models.CharField(max_length=20, unique=True)
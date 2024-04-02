import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):

    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name =  models.CharField(max_length=30)
    last_name =  models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.username = self.email
        self.password = self.set_password(self.password)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)


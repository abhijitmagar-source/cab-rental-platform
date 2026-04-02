from django.db import models
from django.contrib.auth.models import User
from apps.common.models import BaseModel


ROLE_CHOICES = (
    ("OWNER","Owner"),
    ("CUSTOMER","Customer"),
)


class UserProfile(BaseModel):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15,unique=True)

    def __str__(self):
        return self.user.username
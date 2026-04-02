from django.db import models
from apps.common.models import BaseModel
from apps.users.models import UserProfile


class Vehicle(BaseModel):

    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    daily_rate = models.DecimalField(max_digits=10,decimal_places=2)

    is_active = models.BooleanField(default=True)

    def create(self, validated_data):
     images_data = validated_data.pop('images', [])
     vehicle = Vehicle.objects.create(**validated_data)  # Create vehicle first
     for img in images_data:
         VehicleImage.objects.create(vehicle=vehicle, **img)  # Attach images
     return vehicle

    def __str__(self):
        return self.title
    
class VehicleImage(BaseModel):
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicle_images/')
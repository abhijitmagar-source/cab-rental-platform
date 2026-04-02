from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    total_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = ["id","vehicle","start_date","end_date","total_price"]

    def validate(self, data):
        vehicle = data.get("vehicle")
        request = self.context["request"]
        customer = request.user.userprofile
        start = data["start_date"]
        end = data["end_date"]

        if vehicle.owner == customer:
            raise serializers.ValidationError("Owner cannot book his own vehicle")
        
        if end < start:
            raise serializers.ValidationError("End must be after start data")
        
        existing_booking = Booking.objects.filter(vehicle=vehicle)

        for booking in existing_booking:

            if booking.status == "CANCELLED":
                continue

            if booking.start_date<= end and booking.end_date >= start:
                raise serializers.ValidationError("Vehicle already booked")
        
        return data
    

    def create(self,validated_data):
        request = self.context["request"]
        profile = request.user.userprofile
        vehicle = validated_data["vehicle"]
        start = validated_data["start_date"]
        end = validated_data["end_date"]

        days = (end - start).days

        if days == 0:
            days = 1

        total = days * vehicle.daily_rate

        booking = Booking.objects.create(customer=profile,total_price=total,
                                         **validated_data)

        return booking
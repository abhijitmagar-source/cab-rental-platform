from rest_framework import serializers
from .models import Vehicle, VehicleImage


class VehicleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleImage
        fields = ['id', 'image']


class VehicleSerializer(serializers.ModelSerializer):

    images = VehicleImageSerializer(
        source='vehicleimage_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ["owner"]

class VehicleSearchSerializer(serializers.Serializer):

    city = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date >= end_date:
            raise serializers.ValidationError("End date must be greater than start date")

        return data
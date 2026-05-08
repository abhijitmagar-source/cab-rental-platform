from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import UserProfile,ROLE_CHOICES


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    phone = serializers.CharField()

    def create(self,validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )

        profile = UserProfile.objects.create(
            user=user,
            role=validated_data["role"],
            phone=validated_data["phone"]
        )

        return profile
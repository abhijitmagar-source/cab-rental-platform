from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


class RegisterView(APIView):

    @extend_schema(
        summary="Register User",
        description="Create a new user account.",
        request=RegisterSerializer,
        responses={
            200: OpenApiResponse(description="User registered successfully")
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "User registered successfully"
        })
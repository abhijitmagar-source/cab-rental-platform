from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from apps.vehicles.models import Vehicle
from apps.bookings.models import Booking
from .serializers import VehicleSerializer, VehicleSearchSerializer
from rest_framework.pagination import PageNumberPagination


class CreateVehicleView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_profile = request.user.userprofile

        if user_profile.role != 'owner':
            return Response({"error":"Only vehicle owners can add vehicles"})

    
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
    
            serializer.save(owner=request.user.userprofile)
            return Response(serializer.data)

        return Response(serializer.errors)


class MyVehicles(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        vehicles = Vehicle.objects.filter(owner=request.user.userprofile)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)


class SearchVehicle(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VehicleSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        city = serializer.validated_data["city"]
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]

        page = request.GET.get("page", 1)
        cache_key = f"search_{city}_{start_date}_{end_date}_page_{page}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        vehicles = Vehicle.objects.filter(
            city__iexact=city,
            is_active=True
        )

        booked_vehicle_ids = Booking.objects.filter(
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=["PENDING", "CONFIRMED"]
        ).values_list("vehicle_id", flat=True)

        vehicles = vehicles.exclude(id__in=booked_vehicle_ids)

        pagination = PageNumberPagination()
        result_page = pagination.paginate_queryset(vehicles, request)

        serializer = VehicleSerializer(result_page, many=True)
        response = pagination.get_paginated_response(serializer.data)

        cache.set(cache_key, response.data, timeout=60 * 5)

        return Response(response.data)


class ListVehicle(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        page = request.GET.get("page", 1)
        cache_key = f"vehicle_list_{page}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        vehicles = Vehicle.objects.filter(is_active=True)

        pagination = PageNumberPagination()
        result_page = pagination.paginate_queryset(vehicles, request)

        serializer = VehicleSerializer(result_page, many=True)
        response = pagination.get_paginated_response(serializer.data)

        cache.set(cache_key, response.data, timeout=60 * 5)

        return Response(response.data)


class DetailsVehicle(APIView):

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)


class UpdateVehicle(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        vehicle = get_object_or_404(Vehicle, pk=pk)

        if vehicle.owner != request.user.userprofile:
            return Response({"error": "You are not the owner"}, status=403)

        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data)

        return Response(serializer.errors)


class DeleteVehicle(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        vehicle = get_object_or_404(Vehicle, pk=pk)

        if vehicle.owner != request.user.userprofile:
            return Response({"error": "You are not the owner"}, status=403)

        vehicle.delete()
        cache.clear()

        return Response({"message": "Vehicle deleted successfully"})
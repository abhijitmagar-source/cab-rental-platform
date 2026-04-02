from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import BookingSerializer
from .models import Booking
from django.shortcuts import get_object_or_404
from rest_framework import status

class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):

        serializer = BookingSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    


class MyBookingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        bookings = Booking.objects.filter(customer=user_profile)
        serializer = BookingSerializer(bookings, many=True)

        return Response(serializer.data)
    
class CancelBooking(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        booking = get_object_or_404(Booking,pk=pk,customer=request.user.userprofile)

        if booking.status != "PENDING":
            return Response({"error":"Cannot cancel This Booking"},status=status.HTTP_400_BAD_REQUEST)

        booking.status = "CANCELLED"
        booking.save()

        return Response({"message":"Booking cancelled succesfully"})
    

class OwnerBookings(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(
            vehicle__owner=request.user.userprofile
        )
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    
class AcceptBooking(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)

        if booking.vehicle.owner != request.user.userprofile:
            return Response({"error": "Not allowed"}, status=403)

        if booking.status != "PENDING":
            return Response({"error": "Already processed"}, status=400)

        booking.status = "CONFIRMED"
        booking.save()

        return Response({"message": "Booking confirmed"})
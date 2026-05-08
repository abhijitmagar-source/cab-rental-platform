from django.urls import path
from .views import CreateBookingView, MyBookingsView,CancelBooking,OwnerBookings,AcceptBooking

urlpatterns = [

    path('bookvehicle/', CreateBookingView.as_view(), name='create-booking'),
    path('mybookings/', MyBookingsView.as_view(), name='my-bookings'),
    path('<int:pk>/cancel/',CancelBooking.as_view(),name='cancel'),
    path('ownerbookings/',OwnerBookings.as_view(),name='owner-bookings'),
    path('acceptbooking/<int:pk>/',AcceptBooking.as_view(),name='accept')

]
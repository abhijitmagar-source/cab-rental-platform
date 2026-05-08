from django.urls import path
from .views import CreateVehicleView,DetailsVehicle,SearchVehicle,ListVehicle,UpdateVehicle,DeleteVehicle
                        


urlpatterns = [

    path('create/', CreateVehicleView.as_view(), name='create-vehicle'),
    path('list/',ListVehicle.as_view(),name='vehiclelist'),
    path('<int:pk>/',DetailsVehicle.as_view()),
    path("search/", SearchVehicle.as_view(), name="vehicle-search"),
    path('update/<int:pk>/',UpdateVehicle.as_view(),name='update-details'),
    path('delete/<int:pk>/',DeleteVehicle.as_view(),name='remove-vehicle')
    

]
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/vehicles/', include('apps.vehicles.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
    path('schema/',SpectacularAPIView.as_view(),name='schema'),
    path('docs/',SpectacularSwaggerView.as_view(url_name='schema'))


]
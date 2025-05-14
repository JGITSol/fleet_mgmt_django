from django.contrib import admin
from django.urls import path, include

# Import the app-specific url modules to access their urlpatterns and app_name
from vehicles import urls as vehicle_urls
from maintenance import urls as maintenance_urls
from CarFleetManagement.emergency import urls as emergency_urls
# accounts.urls will be handled differently if needed, or assume it has app_name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), # Keep as is for now
    path('api/vehicles/', include((vehicle_urls, 'vehicles'), namespace='vehicles')),
    path('api/maintenance/', include((maintenance_urls, 'maintenance'), namespace='maintenance')),
    path('api/emergency/', include((emergency_urls, 'emergency'), namespace='emergency')),
    path('api/', include(('CarFleetManagement.api.urls', 'CarFleetManagement.api'), namespace='CarFleetManagement.api')),
]

from django.contrib import admin
from django.urls import path, include

# Import the app-specific url modules to access their urlpatterns and app_name
from CarFleetManagement.vehicles import urls as vehicle_urls
from CarFleetManagement.maintenance import urls as maintenance_urls
from CarFleetManagement.emergency import urls as emergency_urls

from django.http import HttpResponse


def root_view(request):
    return HttpResponse("<h2>Welcome to the Car Fleet Management</h2><p>See <a href='/api/'>/api/</a> for API endpoints.</p>")

# NOTE: keep all DRF API endpoints under the /api/ prefix. The web views
# (HTML pages) should be mounted at top-level paths to avoid colliding with
# API routes which previously caused redirects (302) to the login page during tests.
urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),

    # Web app (HTML) views
    path('accounts/', include('CarFleetManagement.accounts.urls')),
    path('vehicles/', include((vehicle_urls, 'vehicles'), namespace='vehicles')),
    path('maintenance/', include((maintenance_urls, 'maintenance'), namespace='maintenance')),
    path('emergency/', include((emergency_urls, 'emergency'), namespace='emergency')),

    # API (DRF) endpoints
    path('api/', include(('CarFleetManagement.api.urls', 'CarFleetManagement.api'), namespace='CarFleetManagement.api')),
]

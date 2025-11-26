from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

from CarFleetManagement.emergency import urls as emergency_urls
from CarFleetManagement.emergency import views as emergency_views
from CarFleetManagement.maintenance import urls as maintenance_urls
from CarFleetManagement.maintenance import views as maintenance_views

# Import view callables for optional non-namespaced aliases (DEV only)
# Import the app-specific url modules to access their urlpatterns and app_name
from django.contrib.auth import views as auth_views
from CarFleetManagement.accounts import views as accounts_views
from CarFleetManagement.vehicles import urls as vehicle_urls
from CarFleetManagement.vehicles import views as vehicle_views


def root_view(request):
    return render(request, 'home.html')

# NOTE: keep all DRF API endpoints under the /api/ prefix. The web views
# (HTML pages) should be mounted at top-level paths to avoid colliding with
# API routes which previously caused redirects (302) to the login page during tests.
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', root_view, name='home'),
    path('admin/', admin.site.urls),

    # Web app (HTML) views - include each app's urls once (non-namespaced)
    path('accounts/', include('CarFleetManagement.accounts.urls')),
    path('vehicles/', include(vehicle_urls)),
    path('maintenance/', include(maintenance_urls)),
    path('emergency/', include(emergency_urls)),

    # API (DRF) endpoints
    path('api/', include(('CarFleetManagement.api.urls', 'CarFleetManagement.api'), namespace='CarFleetManagement.api')),
)

# Backwards-compatible, non-namespaced aliases for legacy templates/tests.
# Always include these for compatibility
urlpatterns += [
    # Auth aliases
    path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', accounts_views.RegisterView.as_view(), name='register'),

    # Vehicles (non-namespaced aliases)
    path('vehicles/', vehicle_views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/<int:pk>/', vehicle_views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('vehicles/create/', vehicle_views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/update/', vehicle_views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', vehicle_views.VehicleDeleteView.as_view(), name='vehicle_delete'),

    # Maintenance (non-namespaced aliases)
    path('maintenance/', maintenance_views.MaintenanceListView.as_view(), name='maintenance_list'),
    path('maintenance/<int:pk>/', maintenance_views.MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('maintenance/create/', maintenance_views.MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('maintenance/<int:pk>/update/', maintenance_views.MaintenanceUpdateView.as_view(), name='maintenance_update'),
    path('maintenance/<int:pk>/delete/', maintenance_views.MaintenanceDeleteView.as_view(), name='maintenance_delete'),

    # Emergency (non-namespaced aliases)
    path('emergency/', emergency_views.EmergencyIncidentListView.as_view(), name='emergency_list'),
    path('emergency/<int:pk>/', emergency_views.EmergencyIncidentDetailView.as_view(), name='emergency_detail'),
    path('emergency/create/', emergency_views.EmergencyIncidentCreateView.as_view(), name='emergency_create'),
    path('emergency/<int:pk>/update/', emergency_views.EmergencyIncidentUpdateView.as_view(), name='emergency_update'),
    path('emergency/<int:pk>/delete/', emergency_views.EmergencyIncidentDeleteView.as_view(), name='emergency_delete'),
    path('emergency/<int:incident_id>/response/create/', emergency_views.EmergencyResponseCreateView.as_view(), name='emergency_response_create'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)

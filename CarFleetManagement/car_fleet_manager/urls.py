"""
URL configuration for car_fleet_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

# Import the view for theme switching
from django.http import JsonResponse

def set_theme(request):
    """View to handle theme switching.
    
    Updates the session with the selected theme preference.
    """
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        request.session['theme'] = theme
        return JsonResponse({'status': 'success', 'theme': theme})
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

urlpatterns = [
    # Include Django's i18n URLs for language switching
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Theme switching URL
    path('set-theme/', set_theme, name='set_theme'),
    
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("features/", TemplateView.as_view(template_name="features.html"), name="features"),
    path("accounts/", include("accounts.urls")),
    path('social-auth/', include('social_django.urls', namespace='social')),
]

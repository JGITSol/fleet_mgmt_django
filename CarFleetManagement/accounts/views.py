from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import CustomUser, UserRole, Driver, EmergencyContact
from vehicles.models import Vehicle
from maintenance.models import Maintenance
from emergency.models import EmergencyIncident
from django.db.models import Count, Sum, Q
from datetime import date, timedelta

# Authentication Views
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Role-based Dashboard Views
@login_required
def dashboard(request):
    """Redirect to the appropriate dashboard based on user role"""
    user = request.user
    
    if not user.role:
        messages.warning(request, 'Your account does not have a role assigned. Please contact an administrator.')
        return redirect('home')
    
    if user.is_admin:
        return redirect('admin_dashboard')
    elif user.is_fleet_manager:
        return redirect('fleet_manager_dashboard')
    elif user.is_driver:
        return redirect('driver_dashboard')
    elif user.is_maintenance_staff:
        return redirect('technician_dashboard')
    else:
        return redirect('home')

# Admin Dashboard
@login_required
def admin_dashboard(request):
    """Dashboard for administrators"""
    if not request.user.is_admin and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get statistics for admin dashboard
    stats = {
        'total_vehicles': Vehicle.objects.count(),
        'total_drivers': Driver.objects.count(),
        'total_users': CustomUser.objects.count(),
        'pending_maintenance': Maintenance.objects.filter(status='SCHEDULED').count(),
        'active_incidents': EmergencyIncident.objects.exclude(status='CLOSED').count(),
    }
    
    # Get recent activities
    recent_incidents = EmergencyIncident.objects.all().order_by('-reported_time')[:5]
    recent_maintenance = Maintenance.objects.all().order_by('-scheduled_date')[:5]
    
    context = {
        'stats': stats,
        'recent_incidents': recent_incidents,
        'recent_maintenance': recent_maintenance,
    }
    
    return render(request, 'dashboard_admin.html', context)

# Fleet Manager Dashboard
@login_required
def fleet_manager_dashboard(request):
    """Dashboard for fleet managers"""
    if not request.user.is_fleet_manager and not request.user.is_admin and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get statistics for fleet manager dashboard
    stats = {
        'active_vehicles': Vehicle.objects.filter(status='AVAILABLE').count(),
        'available_vehicles': Vehicle.objects.filter(status='AVAILABLE').count(),
        'maintenance_vehicles': Vehicle.objects.filter(status='MAINTENANCE').count(),
        'overdue_vehicles': Vehicle.objects.filter(next_service_date__lt=date.today()).count(),
    }
    
    # Get recent activities
    recent_incidents = EmergencyIncident.objects.all().order_by('-reported_time')[:5]
    upcoming_maintenance = Maintenance.objects.filter(status='SCHEDULED').order_by('scheduled_date')[:5]
    
    context = {
        'stats': stats,
        'recent_incidents': recent_incidents,
        'upcoming_maintenance': upcoming_maintenance,
    }
    
    return render(request, 'dashboard_fleet_manager.html', context)

# Driver Dashboard
@login_required
def driver_dashboard(request):
    """Dashboard for drivers"""
    if not request.user.is_driver and not request.user.is_admin and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get driver information
    try:
        driver = Driver.objects.get(user=request.user)
        assigned_vehicle = driver.assigned_vehicles.first()
    except Driver.DoesNotExist:
        driver = None
        assigned_vehicle = None
    
    # Placeholder for tasks (would be replaced with actual task model)
    todays_tasks = []
    upcoming_maintenance = []
    
    if assigned_vehicle:
        upcoming_maintenance = Maintenance.objects.filter(
            vehicle=assigned_vehicle,
            status='SCHEDULED'
        ).order_by('scheduled_date')[:3]
    
    context = {
        'driver': driver,
        'assigned_vehicle': assigned_vehicle,
        'todays_tasks': todays_tasks,
        'upcoming_maintenance': upcoming_maintenance,
    }
    
    return render(request, 'dashboard_driver.html', context)

# Technician Dashboard
@login_required
def technician_dashboard(request):
    """Dashboard for maintenance staff"""
    if not request.user.is_maintenance_staff and not request.user.is_admin and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get statistics for technician dashboard
    today = date.today()
    stats = {
        'pending_tasks': Maintenance.objects.filter(status='SCHEDULED').count(),
        'in_progress_tasks': Maintenance.objects.filter(status='IN_PROGRESS').count(),
        'completed_tasks': Maintenance.objects.filter(status='COMPLETED', completed_date=today).count(),
    }
    
    # Get active maintenance tasks
    active_tasks = Maintenance.objects.filter(
        Q(status='SCHEDULED') | Q(status='IN_PROGRESS')
    ).order_by('scheduled_date')[:10]
    
    context = {
        'stats': stats,
        'active_tasks': active_tasks,
    }
    
    return render(request, 'dashboard_technician.html', context)

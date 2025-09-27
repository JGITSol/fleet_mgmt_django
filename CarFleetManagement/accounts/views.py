from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .models import CustomUser


class RegisterView(CreateView):
    """User registration view"""

    model = CustomUser
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please log in.")
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

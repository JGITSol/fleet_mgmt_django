from django.db import models
from django.utils.translation import gettext_lazy as _
from CarFleetManagement.accounts.models import CustomUser

class WebhookEndpoint(models.Model):
    url = models.URLField(max_length=500, verbose_name=_('Endpoint URL'))
    secret = models.CharField(max_length=255, blank=True, verbose_name=_('Signing Secret'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active?'))
    events = models.JSONField(default=list, help_text=_('List of events this endpoint subscribes to (e.g. emergency.created)'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Webhook Endpoint')
        verbose_name_plural = _('Webhook Endpoints')

    def __str__(self):
        return f"{self.url} ({'Active' if self.is_active else 'Inactive'})"

class WebhookEvent(models.Model):
    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    response_status = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} -> {self.endpoint.url} [{self.response_status}]"

class ChatSession(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chat_sessions')
    title = models.CharField(max_length=255, blank=True, null=True, help_text=_('Optional descriptive title for the session'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title or f"Chat Session {self.id}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Msg from {self.sender.username} at {self.created_at}"

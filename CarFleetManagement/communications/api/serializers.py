from typing import ClassVar
from rest_framework import serializers
from CarFleetManagement.communications.models import WebhookEndpoint, WebhookEvent, ChatSession, ChatMessage
from CarFleetManagement.accounts.serializers import UserSerializer

class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields: ClassVar[list[str]] = ['id', 'url', 'secret', 'is_active', 'events', 'created_at']
        read_only_fields: ClassVar[list[str]] = ['id', 'created_at']

class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields: ClassVar[list[str]] = ['id', 'endpoint', 'event_type', 'payload', 'response_status', 'response_body', 'created_at']
        read_only_fields: ClassVar[list[str]] = ['id', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields: ClassVar[list[str]] = ['id', 'participants', 'title', 'created_at', 'updated_at']
        read_only_fields: ClassVar[list[str]] = ['id', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields: ClassVar[list[str]] = ['id', 'session', 'sender', 'content', 'is_read', 'created_at']
        read_only_fields: ClassVar[list[str]] = ['id', 'created_at']

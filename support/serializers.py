from rest_framework import serializers

from .models import Contact


class ChatMessageSerializer(serializers.Serializer):
    """A single turn in the client-held conversation."""
    role = serializers.ChoiceField(choices=['user', 'assistant'])
    content = serializers.CharField(max_length=4000, allow_blank=False, trim_whitespace=True)


class ChatRequestSerializer(serializers.Serializer):
    """The chat request body: the full conversation so far, re-sent each turn."""
    messages = serializers.ListField(
        child=ChatMessageSerializer(),
        allow_empty=False,
        max_length=20,  # cap the prompt pushed to the provider
    )


class ContactSerializer(serializers.ModelSerializer):
    """Public handoff / contact submission."""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'source', 'conversation']

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('Please enter your name.')
        return value

    def validate_message(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError('Please give us a little more detail (at least 10 characters).')
        return value

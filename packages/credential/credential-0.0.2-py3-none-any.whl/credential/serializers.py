from rest_framework import serializers


class CredentialRenderedFormResponseSerializer(serializers.Serializer):
    form = serializers.CharField()

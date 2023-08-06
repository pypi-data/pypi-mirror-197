from rest_framework import serializers

from .models import HasStatus


class HasStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = HasStatus
        fields = ('status',)

    def get_status(self, obj):
        return obj.get_status

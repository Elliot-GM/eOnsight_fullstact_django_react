from rest_framework import serializers
from .models import Bridge
    
from rest_framework import serializers
from .models import Bridge

class BridgeSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = ['Good', 'Fair', 'Poor', 'Bad']

    class Meta:
        model = Bridge
        fields = ['id', 'name', 'location', 'inspection_date', 'status', 'traffic_load']

    def validate_status(self, value):
        if value not in self.STATUS_CHOICES:
            raise serializers.ValidationError("Invalid status value. Must be one of 'Good', 'Fair', 'Poor', or 'Bad'.")
        return value

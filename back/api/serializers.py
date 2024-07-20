from rest_framework import serializers
from .models import Bridge

class BridgeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bridge model.

    This serializer converts Bridge instances to JSON format and validates data for creating or updating Bridge instances.

    Attributes:
        STATUS_CHOICES (list of str): Allowed values for the status field.
    """
    STATUS_CHOICES = ['Good', 'Fair', 'Poor', 'Bad']

    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = Bridge
        fields = ['id', 'name', 'location', 'inspection_date', 'status', 'traffic_load']

    def validate_status(self, value):
        """
        Validate the status field to ensure it contains a valid value.

        Args:
            value (str): The value to validate.

        Raises:
            serializers.ValidationError: If the value is not in STATUS_CHOICES.

        Returns:
            str: The validated value.
        """
        if value not in self.STATUS_CHOICES:
            raise serializers.ValidationError("Invalid status value. Must be one of 'Good', 'Fair', 'Poor', or 'Bad'.")
        return value

from django.db import models

class Bridge(models.Model):
    """
    Model representing a bridge.

    Attributes:
        name (str): The name of the bridge.
        location (str): The location of the bridge.
        inspection_date (date): The date of the last inspection of the bridge.
        status (str): The current status of the bridge.
        traffic_load (int): The traffic load capacity of the bridge.
    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    inspection_date = models.DateField()
    status = models.CharField(max_length=50)
    traffic_load = models.IntegerField()

    class Meta:
        db_table = 'bridges'

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: The name of the bridge.
        """
        return self.name
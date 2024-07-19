from django.db import models

class Bridge(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    inspection_date = models.DateField()
    status = models.CharField(max_length=50)
    traffic_load = models.IntegerField()

    class Meta:
        db_table = 'bridges'

    def __str__(self):
        return self.name
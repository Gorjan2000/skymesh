from django.db import models

class Location(models.Model):
    node_Id = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    username = models.CharField(max_length=30)
    datetime = models.CharField(max_length=30)

    class Meta:
        db_table = 'location'

    def __str__(self):
        return f"Location {self.node_Id}"



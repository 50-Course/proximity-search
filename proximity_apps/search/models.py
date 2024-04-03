from django.contrib.gis.db import models as gis_models
from django.db import models


class TimeStampMixin(models.Model):
    """
    A mixin class that adds created_at and updated_at fields to a model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


######## MODELS ########

class Town(models.Model):
    """
    Represents a town or city a facebook community or group is located in
    """
    name = models.CharField(max_length=100)
    location = gis_models.PointField()

    def __str__(self) -> str:
        return f'{self.name}'


class Group(models.Model):
    """
    Represents a facebook group or community
    """
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    location = gis_models.PointField()
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    is_private = models.BooleanField()
    member_count = models.IntegerField()
    categories = models.JSONField() # Essentially, a group can belong to more than one categor
                                    # Could be education and social for example
                                    # Or technology and social
                                    # Or just social

    class Meta:
        verbose_name_plural = 'Groups'
        ordering = ['-created_at']
        filters = ['town']

    def __str__(self) -> str:
        return f'{self.name}'

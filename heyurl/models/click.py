from django.db import models

from .url import Url


class Click(models.Model):
    """
    Keeps track of the clicks on a short URL
    """
    class JSONAPIMeta:
        resource_name = "metrics"

    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    browser = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')

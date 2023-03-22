import random
import string
from typing import Optional

from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone


class Url(models.Model):
    """
    Keep track of the short and original urls
    """
    class JSONAPIMeta:
        resource_name = "urls"

    short_url = models.CharField(max_length=255)
    original_url = models.CharField(max_length=255)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')

    @staticmethod
    def is_valid_url(url) -> Optional[str]:
        """
        Check if the url is valid and unique
        :param url: to validate
        :return: str: error message if not valid
        """
        validate = URLValidator()
        try:
            validate(url)
        except:
            return 'The Original URL is not valid!'

        # check if the url is unique
        if Url.objects.filter(original_url=url).exists():
            return 'The Original URL already exists!'

    @staticmethod
    def generate_short_url():
        """
        Generate a short url of max 5 characters
        :return: str new short_url
        """

        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 5)))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Check if it is a create and create a short_url
        if not self.pk:
            new_short_url = None
            # Get all the short_urls
            short_urls = list(Url.objects.values_list('short_url', flat=True))
            while new_short_url is None:
                short_url = Url.generate_short_url()

                # Check if the short_url is unique
                if short_url not in short_urls:
                    new_short_url = short_url

            # Set the short_url
            self.short_url = new_short_url

            # Set the created_at and updated_at fields
            self.created_at = self.updated_at = timezone.now()
        else:
            # Update the updated_at field
            self.updated_at = timezone.now()

        super().save(force_insert, force_update, using, update_fields)

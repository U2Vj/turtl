from django.db import models
from django.urls import reverse


class Room(models.Model):
    image = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return self.image

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('room-detail', args=[str(self.image)])




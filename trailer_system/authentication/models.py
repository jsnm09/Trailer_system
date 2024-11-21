from django.db import models

# Create your models here.

class Trailer(models.Model):
    name = models.CharField(max_length=100)  # Name of the trailer
    status = models.CharField(max_length=50)  # Status, e.g., "In Yard," "In Transit"
    rented_by = models.CharField(max_length=100, blank=True, null=True)  # Who rented it
    rent_due = models.DateField(blank=True, null=True)  # Due date for rent return

    def __str__(self):
        return self.name

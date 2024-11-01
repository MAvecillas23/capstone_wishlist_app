from django.db import models

# similar to PeeWee create db here
class Place(models.Model):
    name = models.CharField(max_length=200)  # character field for location name
    visited = models.BooleanField(default=False) # bool for visited or not

    def __str__(self):
        return f'{self.name} visted? {self.visited}'










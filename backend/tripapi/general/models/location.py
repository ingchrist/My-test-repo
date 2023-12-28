from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.address}, {self.state}'

    class Meta:
        ordering = ('state',)
        verbose_name_plural = 'Locations'

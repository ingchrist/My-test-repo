from typing import Type
from django.db import models
from os.path import join


def upload_to(instance: Type["Testimonial"], filename: str):
    """
    Create unique path to upload image for Testimonial instance

    :param instance: Testimonial instance
    :type instance: Testimonial
    :param filename: Image filename e.g image.jpg
    :type filename: str
    :return: Path to upload image
    :rtype: str
    """
    return join('testimonials', str(instance.id), filename)


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    testimonial = models.TextField()
    image = models.ImageField(upload_to=upload_to, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)

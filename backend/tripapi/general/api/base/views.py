from general.models import Location, Testimonial
from project_api_key.permissions import HasProjectAPIKey
from rest_framework import generics

from . import serializers


class ListLocations(generics.ListAPIView):
    serializer_class = serializers.LocationSerializer
    permission_classes = [HasProjectAPIKey]

    def get_queryset(self):
        return Location.objects.all()


class ListTestimonials(generics.ListAPIView):
    serializer_class = serializers.TestimonialSerializer
    permission_classes = [HasProjectAPIKey]

    def get_queryset(self):
        return Testimonial.objects.all()

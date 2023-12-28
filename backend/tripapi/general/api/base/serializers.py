from rest_framework import serializers

from general.models import Location, Testimonial


class LocationSerializer(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ["direction"]

    def get_direction(self, obj: Location):
        return f'{obj.address}, {obj.state}'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["name", "testimonial", "image"]

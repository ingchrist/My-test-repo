from django.contrib import admin

from .models import Location, Testimonial

admin.site.register([Location, Testimonial])

from django.urls import path

from . import views

app_name = 'general'

urlpatterns = [
    path('locations/', views.ListLocations.as_view(), name='list-locations'),
    path(
        'testimonials/',
        views.ListTestimonials.as_view(),
        name='list-testimonials'),
]

import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


base_schema_view = get_schema_view(
    openapi.Info(
        title="TripValue Project API",
        default_version='v1',
        description="Api documentation for all of the endpoints\
available from TripValue.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@tripvalue.com.ng"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator
)


doc_urls = [
    path(
        'docs/',
        base_schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
]


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include(
        [
            path('account/', include('account.api.base.urls')),
            path('payment/', include('payment.api.base.urls')),
            path('cargo/', include('cargo.api.base.urls')),
            path('transport/', include('transport.api.base.urls')),
            path('general/', include('general.api.base.urls')),
        ])
    ),


    # add restframework urls
    path('api-auth/', include('rest_framework.urls')),
]

# Append all url patterns together
urlpatterns = doc_urls + urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        # Debug toolbar url
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)

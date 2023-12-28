from django.urls import include, path
from utils.base.routers import CustomDefaultRouter

from . import views

app_name = 'cargo'

router = CustomDefaultRouter()

router.register(
    r'drivers',
    views.DriverViewSet,
    basename='driver'
)

urlpatterns = [
    path('', include(router.urls)),
    path('packages/', views.UserPackageList.as_view(), name='packages'),
    path(
        'packages/search/by-tracking-code/',
        views.SearchPackageByTrackingCode.as_view(),
        name='search-packages-by-tracking-code'),
    path('packages/create/', views.PackageCreate.as_view(),
         name='package-create'),
    path('packages/get-price-packages/<str:tracking_code>/',
         views.GetPricePackages.as_view(), name='get-price-packages'),
    path('packages/create-order/', views.SelectLogisticsPackage.as_view(),
         name='create-package-order'),
    path('packages/cargo-types/',
         views.PackageCargoType.as_view(), name='cargo-types'),
    path('packages/rud/<str:tracking_code>/',
         views.UserPackageRetrieveUpdate.as_view(), name='package-rud'),
    path('packages/rud/pkg-code/<str:tracking_code>/',
         views.UserPackageRetrieveUpdateByPkg.as_view(),
         name='package-rud-pkg-code'),
    path('packages/rud/nath-pkg-code/<str:tracking_code>/',
         views.SuperUserPackageRetrieveUpdate.as_view(),
         name='package-rud-pkg-code-no-auth'),

    path('orders/', views.UserOrderList.as_view(), name='orders'),
    path('orders/detail/<str:tracking_code>/',
         views.OrderDetailView.as_view(), name='order-detail'),

    path('orders/logistics/recent/', views.LogisticOrderList.as_view(),
         name='orders-logistics-recent'),

    path('orders/logistics/update/<str:tracking_code>/',
         views.LogisticOrderUpdateView.as_view(),
         name='orders-logistics-update'),

    path('logistics-update/', views.LogisticsUpdateView.as_view(),
         name="logistics-update"),

    path('logistics/upload-logo/', views.LogisticsCreateImageView.as_view(),
         name="logistics/upload-logo/"),

    path('price-package-create/', views.PricePackageCreate.as_view(),
         name="price-package-create"),

    path('price-package-update/<str:tracking_code>/',
         views.PricePackageUpdate.as_view(),
         name="price-package-update"),

    path('price-package-delete/<str:tracking_code>/',
         views.PricePackageDelete.as_view(),
         name="price-package-delete"),

    path('packages/track/<str:tracking_code>/',
         views.LogisticPackageRetrieve.as_view(),
         name='track-package'),

    path('price-package-orders/<str:tracking_code>/orders/',
         views.OrdersForPricePackage.as_view(),
         name="price-package-orders"),

    path('vehicle-create/', views.VehicleCreate.as_view(),
         name="vehicle-create"),

    path('vehicle-list-all/', views.VehiclesList.as_view(),
         name="vehicle-list-all"),

    path('vehicle-update/<str:tag>/',
         views.VehiclesUpdate.as_view(),
         name="vehicle-update"),

    path('vehicle-delete/<str:tag>/',
         views.VehiclesDelete.as_view(),
         name="vehicle-delete"),

    path('vehicle-list-by-plate-number/',
         views.VehiclesListByPlateNumber.as_view(),
         name="vehicle-list-by-plate-number"),

    path('packages/list-by-tracking-code/<str:tracking_code>/',
         views.PackageListByTrackingCode.as_view(),
         name='package-list-by-tracking-code'),

]

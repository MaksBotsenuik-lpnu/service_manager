from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    DeviceListView, DeviceDetailView, DeviceCreateView, DeviceUpdateView, DeviceDeleteView,
    ServiceListView, ServiceDetailView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView,
    RepairOrderListView, RepairOrderDetailView, RepairOrderCreateView, RepairOrderUpdateView, RepairOrderDeleteView,
    PartListView, PartDetailView, PartCreateView, PartUpdateView, PartDeleteView,
    get_client_devices,
)
from .api_views import (
    ClientViewSet, DeviceViewSet, ServiceViewSet,
    RepairOrderViewSet, PartViewSet
)

app_name = 'service'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'api/clients', ClientViewSet)
router.register(r'api/devices', DeviceViewSet)
router.register(r'api/services', ServiceViewSet)
router.register(r'api/repair-orders', RepairOrderViewSet)
router.register(r'api/parts', PartViewSet)

urlpatterns = [
    # Public API for client devices
    path('public/clients/<int:client_id>/devices/', get_client_devices, name='client-devices'),

    # API URLs (DRF router)
    path('', include(router.urls)),

    # Client URLs
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/new/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

    # Device URLs
    path('devices/', DeviceListView.as_view(), name='device-list'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('devices/new/', DeviceCreateView.as_view(), name='device-create'),
    path('devices/<int:pk>/edit/', DeviceUpdateView.as_view(), name='device-update'),
    path('devices/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),

    # Service URLs
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/new/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),

    # Repair Order URLs
    path('repairs/', RepairOrderListView.as_view(), name='repair-order-list'),
    path('repairs/<int:pk>/', RepairOrderDetailView.as_view(), name='repair-order-detail'),
    path('repairs/new/', RepairOrderCreateView.as_view(), name='repair-order-create'),
    path('repairs/<int:pk>/edit/', RepairOrderUpdateView.as_view(), name='repair-order-update'),
    path('repairs/<int:pk>/delete/', RepairOrderDeleteView.as_view(), name='repair-order-delete'),

    # Part URLs
    path('parts/', PartListView.as_view(), name='part-list'),
    path('parts/<int:pk>/', PartDetailView.as_view(), name='part-detail'),
    path('parts/new/', PartCreateView.as_view(), name='part-create'),
    path('parts/<int:pk>/edit/', PartUpdateView.as_view(), name='part-update'),
    path('parts/<int:pk>/delete/', PartDeleteView.as_view(), name='part-delete'),
] 
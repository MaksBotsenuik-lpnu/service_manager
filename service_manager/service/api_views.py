from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Client, Device, Service, RepairOrder, Part
from .serializers import (
    ClientSerializer, DeviceSerializer, ServiceSerializer,
    RepairOrderSerializer, PartSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing clients
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        operation_description="Get all devices for a specific client",
        responses={
            200: DeviceSerializer(many=True),
            404: "Client not found"
        }
    )
    @action(detail=True, methods=['get'])
    def devices(self, request, pk=None):
        client = self.get_object()
        devices = Device.objects.filter(client=client)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing devices
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing services
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class RepairOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing repair orders
    """
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # Save many-to-many services if provided
        services = self.request.data.getlist('services')
        if services:
            instance.services.set(services)
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        services = self.request.data.getlist('services')
        if services:
            instance.services.set(services)
        instance.save()

    @swagger_auto_schema(
        operation_description="Get all repair orders for a specific client",
        responses={
            200: RepairOrderSerializer(many=True),
            404: "Client not found"
        }
    )
    @action(detail=False, methods=['get'])
    def client_orders(self, request):
        client_id = request.query_params.get('client_id')
        if not client_id:
            return Response({"error": "client_id parameter is required"}, status=400)
        
        orders = self.queryset.filter(client_id=client_id)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class PartViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing parts
    """
    queryset = Part.objects.all()
    serializer_class = PartSerializer

    @swagger_auto_schema(
        operation_description="Get parts by status",
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Part status (available, low_stock, out_of_stock, discontinued)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: PartSerializer(many=True),
            400: "Invalid status parameter"
        }
    )
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status = request.query_params.get('status')
        if not status:
            return Response({"error": "status parameter is required"}, status=400)
        
        if status not in dict(Part.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)
        
        parts = self.queryset.filter(status=status)
        serializer = self.get_serializer(parts, many=True)
        return Response(serializer.data) 
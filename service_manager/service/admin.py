from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Client, Device, Service, RepairOrder, Part,
    RepairOrderService, ServiceToPart
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('client', 'device_type', 'brand', 'model', 'serial_number', 'created_at')
    search_fields = ('brand', 'model', 'serial_number', 'client__first_name', 'client__last_name')
    list_filter = ('device_type', 'created_at')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'estimated_time', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'device', 'get_services', 'status', 'assigned_to', 'created_at')
    search_fields = ('client__first_name', 'client__last_name', 'device__brand', 'device__model')
    list_filter = ('status', 'created_at', 'assigned_to')
    raw_id_fields = ('client', 'device', 'assigned_to')

    def get_services(self, obj):
        return ", ".join([ros.service.name for ros in obj.order_services.all()])
    get_services.short_description = 'Services'


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('part_type', 'brand', 'name', 'price', 'stock_quantity', 'status', 'created_at')
    search_fields = ('brand', 'name', 'description')
    list_filter = ('part_type', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RepairOrderService)
class RepairOrderServiceAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'service')
    search_fields = ('repair_order__id', 'service__name')


@admin.register(ServiceToPart)
class ServiceToPartAdmin(admin.ModelAdmin):
    list_display = ('service', 'part', 'part_amount')
    search_fields = ('service__name', 'part__name')

from django.db import models
from django.utils.translation import gettext_lazy as _

from authenticate.models import User


class Client(models.Model):
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150)
    email = models.EmailField(_("Email"), unique=True)
    phone = models.CharField(_("Phone Number"), max_length=20)
    address = models.TextField(_("Address"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Device(models.Model):
    DEVICE_TYPES = [
        ('laptop', _('Laptop')),
        ('desktop', _('Desktop')),
        ('tablet', _('Tablet')),
        ('smartphone', _('Smartphone')),
        ('other', _('Other')),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='devices',
        verbose_name=_("Client")
    )
    device_type = models.CharField(
        _("Device Type"),
        max_length=20,
        choices=DEVICE_TYPES
    )
    brand = models.CharField(_("Brand"), max_length=100)
    model = models.CharField(_("Model"), max_length=100)
    serial_number = models.CharField(_("Serial Number"), max_length=100, blank=True)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.client.get_full_name()})"


class Service(models.Model):
    SERVICE_TYPES = [
        ('hardware', _('Hardware Repair')),
        ('software', _('Software Repair')),
        ('diagnostic', _('Diagnostic')),
        ('maintenance', _('Maintenance')),
        ('upgrade', _('Upgrade')),
        ('other', _('Other')),
    ]

    name = models.CharField(_("Service Name"), max_length=200)
    service_type = models.CharField(
        _("Service Type"),
        max_length=20,
        choices=SERVICE_TYPES,
        default='hardware'
    )
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    estimated_time = models.DurationField(_("Estimated Time"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['name']

    def __str__(self):
        return self.name


class RepairOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('waiting_for_parts', _('Waiting for Parts')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='repair_orders',
        verbose_name=_('Client')
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='repair_orders',
        verbose_name=_('Device')
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_repairs',
        verbose_name=_('Assigned To')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    description = models.TextField(_('Description'))
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    completed_at = models.DateTimeField(_('Completed At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Repair Order')
        verbose_name_plural = _('Repair Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.client.get_full_name()} - {self.device}"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)


class RepairOrderService(models.Model):
    repair_order = models.ForeignKey('RepairOrder', on_delete=models.CASCADE, related_name='repair_order_services')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='service_repair_orders')
    # Optionally, add fields like quantity, notes, etc.

    class Meta:
        unique_together = ('repair_order', 'service')
        verbose_name = 'RepairOrder-Service Link'
        verbose_name_plural = 'RepairOrder-Service Links'

    def __str__(self):
        return f"{self.repair_order} - {self.service}"


class Part(models.Model):
    PART_TYPES = [
        ('cpu', _('CPU')),
        ('gpu', _('GPU')),
        ('ram', _('RAM')),
        ('motherboard', _('Motherboard')),
        ('storage', _('Storage')),
        ('psu', _('Power Supply')),
        ('cooling', _('Cooling')),
        ('other', _('Other')),
    ]

    name = models.CharField(_("Part Name"), max_length=200)
    part_type = models.CharField(
        _("Part Type"),
        max_length=20,
        choices=PART_TYPES
    )
    brand = models.CharField(_("Brand"), max_length=100)
    model = models.CharField(_("Model"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    minimum_quantity = models.PositiveIntegerField(_("Minimum Quantity"), default=1)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        ordering = ['part_type', 'brand', 'name']

    def __str__(self):
        return f"{self.brand} {self.name} ({self.get_part_type_display()})"

    def is_low_stock(self):
        return self.quantity <= self.minimum_quantity


class ServicePart(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='service_parts')
    part = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='part_services')
    # Optionally, add fields like quantity, notes, etc.

    class Meta:
        unique_together = ('service', 'part')
        verbose_name = 'Service-Part Link'
        verbose_name_plural = 'Service-Part Links'

    def __str__(self):
        return f"{self.service} - {self.part}"


class ServiceToPart(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='service_to_parts')
    part = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='part_to_services')
    part_amount = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('service', 'part')
        verbose_name = 'Service to Part'
        verbose_name_plural = 'Service to Parts'

    def __str__(self):
        return f"{self.service} - {self.part} (x{self.part_amount})"

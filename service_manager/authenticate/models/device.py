from django.db import models
from django.utils.translation import gettext_lazy as _

from authenticate.models.client import Client


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
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .part import Part

class Service(models.Model):
    SERVICE_TYPES = [
        ('repair', _('Repair')),
        ('maintenance', _('Maintenance')),
        ('upgrade', _('Upgrade')),
        ('diagnostic', _('Diagnostic')),
        ('cleaning', _('Cleaning')),
        ('other', _('Other')),
    ]

    name = models.CharField(_("Name"), max_length=200)
    service_type = models.CharField(_("Service Type"), max_length=20, choices=SERVICE_TYPES, default='repair')
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    estimated_time = models.DurationField(_("Estimated Time"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    parts = models.ManyToManyField(Part, through='ServiceToPart', related_name='services')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['name'] 
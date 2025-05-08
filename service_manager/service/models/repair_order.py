from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class RepairOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('waiting_for_parts', _('Waiting for Parts')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='repair_orders',
        verbose_name=_("Client")
    )
    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE,
        related_name='repair_orders',
        verbose_name=_("Device")
    )
    services = models.ManyToManyField(
        'Service',
        through='RepairOrderService',
        related_name='repair_orders',
        verbose_name=_('Services'),
        blank=True
    )
    assigned_to = models.ForeignKey(
        'authenticate.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_repairs',
        verbose_name=_("Assigned To")
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    description = models.TextField(_("Description"))
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    completed_at = models.DateTimeField(_("Completed At"), null=True, blank=True)
    final_sum = models.DecimalField(_('Final Sum'), max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.client.get_full_name()} - {self.device}"

    def save(self, *args, **kwargs):
        # First save to get an ID
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

        # Now calculate the final sum after we have an ID
        service_sum = sum(s.price for s in self.services.all())
        if self.final_sum != service_sum:
            self.final_sum = service_sum
            super().save(update_fields=['final_sum'])

    class Meta:
        verbose_name = _("Repair Order")
        verbose_name_plural = _("Repair Orders")
        ordering = ['-created_at'] 
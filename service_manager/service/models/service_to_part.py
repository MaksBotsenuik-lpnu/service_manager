from django.db import models
from .service import Service
from .part import Part

class ServiceToPart(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_parts')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='part_services')
    part_amount = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('service', 'part')
        verbose_name = 'Service to Part'
        verbose_name_plural = 'Service to Parts'

    def __str__(self):
        return f"{self.service} requires {self.part_amount} x {self.part}" 
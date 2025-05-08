from django.db import models
from .repair_order import RepairOrder
from .service import Service

class RepairOrderService(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name='order_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_orders')
    # Add extra fields if needed, e.g., price, status, etc.

    class Meta:
        unique_together = ('repair_order', 'service')
        verbose_name = 'Repair Order Service'
        verbose_name_plural = 'Repair Order Services'

    def __str__(self):
        return f"{self.repair_order} includes {self.service}" 
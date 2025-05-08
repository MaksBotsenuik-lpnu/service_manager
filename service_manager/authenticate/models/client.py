from django.db import models
from django.utils.translation import gettext_lazy as _


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
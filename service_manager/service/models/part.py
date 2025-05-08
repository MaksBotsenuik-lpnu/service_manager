from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django import forms
from datetime import timedelta

class Part(models.Model):
    PART_TYPES = [
        ('CPU', 'CPU'),
        ('GPU', 'Graphics Card'),
        ('RAM', 'Memory'),
        ('MB', 'Motherboard'),
        ('PSU', 'Power Supply'),
        ('HDD', 'Hard Drive'),
        ('SSD', 'Solid State Drive'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('available', _('Available')),
        ('low_stock', _('Low Stock')),
        ('out_of_stock', _('Out of Stock')),
        ('discontinued', _('Discontinued')),
    ]

    part_type = models.CharField(_('Part Type'), max_length=10, choices=PART_TYPES)
    brand = models.CharField(_('Brand'), max_length=100)
    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(_('Stock Quantity'), default=0)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(_('Created At'), default=timezone.now)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    reserved_parts = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Reserved Parts')

    def __str__(self):
        return f"{self.brand} {self.name}"

    @property
    def is_available(self):
        return self.status == 'available' and self.stock_quantity > 0

    class Meta:
        verbose_name = _('Part')
        verbose_name_plural = _('Parts')
        ordering = ['brand', 'name']

class HoursToTimedeltaField(forms.Field):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            hours = float(value)
            return timedelta(hours=hours)
        except (ValueError, TypeError):
            raise forms.ValidationError("Enter a valid number of hours.")

class ServiceForm(forms.ModelForm):
    estimated_time = HoursToTimedeltaField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Hours'}),
        label='Estimated Time (hours)'
    )
    # ... rest of your form ... 
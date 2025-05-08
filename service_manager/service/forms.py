from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
import logging
from datetime import timedelta

from .models import Client, Device, Service, RepairOrder, Part, ServiceToPart, RepairOrderService
from .models.part import HoursToTimedeltaField

logger = logging.getLogger(__name__)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['client', 'device_type', 'brand', 'model', 'serial_number', 'description']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'device_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ServiceForm(forms.ModelForm):
    estimated_time = HoursToTimedeltaField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Hours'}),
        label='Estimated Time (hours)'
    )
    class Meta:
        model = Service
        fields = ['name', 'service_type', 'description', 'price', 'estimated_time', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaned data: {cleaned_data}")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        logger.debug(f"Instance before save: {instance.__dict__}")
        if commit:
            instance.save()
            logger.debug(f"Instance after save: {instance.__dict__}")
        return instance

    def clean_estimated_time(self):
        value = self.cleaned_data['estimated_time']
        # If value is already a timedelta, return as is
        if isinstance(value, timedelta):
            return value
        # If value is a number (int, float, or string), treat as hours
        try:
            hours = float(value)
            return timedelta(hours=hours)
        except (ValueError, TypeError):
            return value


class RepairOrderForm(forms.ModelForm):
    class Meta:
        model = RepairOrder
        fields = ['client', 'device', 'description', 'notes', 'status', 'assigned_to']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'device': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].required = True
        self.fields['device'].required = True
        # Only show devices for the selected client
        client_id = (
            self.initial.get('client')
            or self.data.get('client')
            or (self.instance.client_id if self.instance and self.instance.pk else None)
        )
        if client_id:
            self.fields['device'].queryset = Device.objects.filter(client_id=client_id)
        else:
            self.fields['device'].queryset = Device.objects.none()
        # Always include the current device in the queryset
        if self.instance.pk:
            device_qs = Device.objects.filter(client=self.instance.client)
            if self.instance.device and self.instance.device not in device_qs:
                device_qs = Device.objects.filter(pk=self.instance.device.pk) | device_qs
            self.fields['device'].queryset = device_qs.distinct()
            self.fields['client'].disabled = True
            self.fields['device'].disabled = True
        # Hide status field on create
        if self.instance.pk is None:
            self.fields['status'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        device = cleaned_data.get('device')
        if client and device and device.client != client:
            raise forms.ValidationError("Selected device does not belong to the selected client.")
        return cleaned_data


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['part_type', 'brand', 'name', 'description', 'price', 'stock_quantity', 'status']
        widgets = {
            'part_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


ServiceToPartFormSet = inlineformset_factory(
    Service,
    ServiceToPart,
    fields=['part', 'part_amount'],
    extra=1,
    can_delete=True,
    min_num=0,  # Allow zero parts
    validate_min=True,
    widgets={
        'part': forms.Select(attrs={'class': 'form-control'}),
        'part_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    }
)


class RepairOrderServiceForm(forms.ModelForm):
    class Meta:
        model = RepairOrderService
        fields = ['service']  # Add extra fields here if needed
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

RepairOrderServiceFormSet = inlineformset_factory(
    parent_model=RepairOrder,
    model=RepairOrderService,
    form=RepairOrderServiceForm,
    extra=1,
    can_delete=True,
) 